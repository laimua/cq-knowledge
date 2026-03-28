# API Routes

"""FastAPI route handlers for Cq Web API."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from cq.core.models import Feedback, KnowledgeUnit, ListFilter, Source
from cq.core.storage import Database, get_database
from cq.repositories.feedback import FeedbackRepository
from cq.repositories.knowledge import KnowledgeRepository

api_router = APIRouter()


# ===== Request/Response Schemas =====


class KnowledgeCreateRequest(BaseModel):
    """Request model for creating a knowledge unit."""

    title: str = Field(..., max_length=200, description="Knowledge title")
    problem: str = Field(..., max_length=2000, description="Problem description")
    solution: str = Field(..., max_length=5000, description="Solution description")
    tags: list[str] = Field(default_factory=list, description="Tags for the knowledge")
    confidence: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Confidence level (0-1)"
    )
    source: str = Field(default="manual", description="Source of the knowledge")


class KnowledgeResponse(BaseModel):
    """Response model for a knowledge unit."""

    id: str
    title: str
    problem: str
    solution: str
    context: dict
    confidence: float
    usage_count: int
    created_at: datetime
    updated_at: datetime
    source: str
    verified: bool
    tags: list[str] = []

    @classmethod
    def from_ku(cls, ku: KnowledgeUnit) -> "KnowledgeResponse":
        """Create response from KnowledgeUnit model.

        Args:
            ku: KnowledgeUnit instance

        Returns:
            KnowledgeResponse instance
        """
        return cls(
            id=ku.id,
            title=ku.title,
            problem=ku.problem,
            solution=ku.solution,
            context=ku.context,
            confidence=ku.confidence,
            usage_count=ku.usage_count,
            created_at=ku.created_at,
            updated_at=ku.updated_at,
            source=ku.source.value,
            verified=ku.verified,
            tags=ku.get_tags(),
        )


class FeedbackRequest(BaseModel):
    """Request model for submitting feedback."""

    helpful: bool = Field(..., description="Whether the knowledge was helpful")
    source: str | None = Field(default=None, description="Optional comment or source")


class FeedbackStatsResponse(BaseModel):
    """Response model for feedback statistics."""

    helpful_count: int
    not_helpful_count: int
    total_count: int


# ===== Dependency Injection =====


async def get_ku_repo(db: Database = Depends(get_database)) -> KnowledgeRepository:
    """Get KnowledgeRepository instance.

    Args:
        db: Database instance

    Returns:
        KnowledgeRepository instance
    """
    return KnowledgeRepository(db)


async def get_feedback_repo(
    db: Database = Depends(get_database),
    ku_repo: KnowledgeRepository = Depends(get_ku_repo),
) -> FeedbackRepository:
    """Get FeedbackRepository instance.

    Args:
        db: Database instance
        ku_repo: KnowledgeRepository instance for confidence updates

    Returns:
        FeedbackRepository instance
    """
    return FeedbackRepository(db, ku_repo=ku_repo)


# ===== Route Handlers =====


@api_router.get("/knowledge", response_model=list[KnowledgeResponse])
async def list_knowledge(
    search: str | None = Query(None, description="Search query for FTS5 search"),
    tags: str | None = Query(None, description="Comma-separated tag filter"),
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Skip first N results"),
    repo: KnowledgeRepository = Depends(get_ku_repo),
) -> list[KnowledgeResponse]:
    """List knowledge units with optional search and filtering.

    Args:
        search: Optional search query - uses FTS5 if provided
        tags: Comma-separated tag filter
        limit: Maximum number of results
        offset: Number of results to skip
        repo: KnowledgeRepository instance

    Returns:
        List of knowledge units
    """
    if search:
        # Use FTS5 full-text search
        tag_list = tags.split(",") if tags else None
        results = await repo.search(
            query=search,
            tags=tag_list,
            limit=limit,
        )
        return [KnowledgeResponse.from_ku(r.knowledge) for r in results]
    else:
        # Use list with filters
        filters: ListFilter | None = None
        if tags:
            filters = ListFilter(tags=tags.split(","))
        kus = await repo.list(filters=filters, limit=limit, offset=offset)
        return [KnowledgeResponse.from_ku(ku) for ku in kus]


@api_router.get("/knowledge/{ku_id}", response_model=KnowledgeResponse)
async def get_knowledge(
    ku_id: str,
    repo: KnowledgeRepository = Depends(get_ku_repo),
) -> KnowledgeResponse:
    """Get a knowledge unit by ID.

    Args:
        ku_id: Knowledge unit ID
        repo: KnowledgeRepository instance

    Returns:
        Knowledge unit details

    Raises:
        HTTPException: If knowledge unit not found
    """
    ku = await repo.get(ku_id)
    if ku is None:
        raise HTTPException(status_code=404, detail="Knowledge unit not found")
    return KnowledgeResponse.from_ku(ku)


@api_router.post("/knowledge", response_model=KnowledgeResponse, status_code=201)
async def create_knowledge(
    request: KnowledgeCreateRequest,
    repo: KnowledgeRepository = Depends(get_ku_repo),
) -> KnowledgeResponse:
    """Create a new knowledge unit.

    Args:
        request: Knowledge creation request
        repo: KnowledgeRepository instance

    Returns:
        Created knowledge unit
    """
    ku = KnowledgeUnit(
        title=request.title,
        problem=request.problem,
        solution=request.solution,
        context={"tags": request.tags} if request.tags else {},
        confidence=request.confidence,
        source=Source(request.source),
    )
    created = await repo.create(ku)
    return KnowledgeResponse.from_ku(created)


@api_router.delete("/knowledge/{ku_id}", status_code=204)
async def delete_knowledge(
    ku_id: str,
    repo: KnowledgeRepository = Depends(get_ku_repo),
) -> None:
    """Delete a knowledge unit.

    Args:
        ku_id: Knowledge unit ID
        repo: KnowledgeRepository instance

    Raises:
        HTTPException: If knowledge unit not found
    """
    success = await repo.delete(ku_id)
    if not success:
        raise HTTPException(status_code=404, detail="Knowledge unit not found")


@api_router.post("/knowledge/{ku_id}/feedback", response_model=FeedbackStatsResponse)
async def add_feedback(
    ku_id: str,
    request: FeedbackRequest,
    ku_repo: KnowledgeRepository = Depends(get_ku_repo),
    feedback_repo: FeedbackRepository = Depends(get_feedback_repo),
) -> FeedbackStatsResponse:
    """Add feedback for a knowledge unit.

    Args:
        ku_id: Knowledge unit ID
        request: Feedback request
        ku_repo: KnowledgeRepository instance
        feedback_repo: FeedbackRepository instance

    Returns:
        Updated feedback statistics

    Raises:
        HTTPException: If knowledge unit not found
    """
    # Verify knowledge unit exists
    ku = await ku_repo.get(ku_id)
    if ku is None:
        raise HTTPException(status_code=404, detail="Knowledge unit not found")

    # Create feedback
    feedback = Feedback(
        ku_id=ku_id,
        helpful=request.helpful,
        source=request.source,
    )
    await feedback_repo.create(feedback)

    # Return updated stats
    stats = await feedback_repo.get_feedback_stats(ku_id)
    return FeedbackStatsResponse(**stats)


@api_router.get("/knowledge/{ku_id}/feedback", response_model=FeedbackStatsResponse)
async def get_feedback_stats(
    ku_id: str,
    feedback_repo: FeedbackRepository = Depends(get_feedback_repo),
) -> FeedbackStatsResponse:
    """Get feedback statistics for a knowledge unit.

    Args:
        ku_id: Knowledge unit ID
        feedback_repo: FeedbackRepository instance

    Returns:
        Feedback statistics
    """
    stats = await feedback_repo.get_feedback_stats(ku_id)
    return FeedbackStatsResponse(**stats)


@api_router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Status message
    """
    return {"status": "healthy", "service": "cq-knowledge-api"}
