# Core Data Models

"""Pydantic models for knowledge management."""

import json
import secrets
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class Source(str, Enum):
    """Knowledge unit source."""
    MANUAL = "manual"
    CLAUDE_CODE = "claude-code"


class KnowledgeUnit(BaseModel):
    """Knowledge unit model.

    Represents a piece of knowledge with problem and solution.
    """

    id: str = Field(
        default_factory=lambda: f"ku_{secrets.token_hex(4)}",
        description="Unique identifier (ku_XXXXXXXX)"
    )
    title: str = Field(..., max_length=200, description="Knowledge title")
    problem: str = Field(..., max_length=2000, description="Problem description")
    solution: str = Field(..., max_length=5000, description="Solution description")
    context: dict = Field(
        default_factory=dict,
        description="Additional context (tags, framework, etc.)"
    )
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence level (0-1)"
    )
    usage_count: int = Field(
        default=0,
        ge=0,
        description="Number of times used"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )
    source: Source = Field(
        default=Source.MANUAL,
        description="Source of the knowledge"
    )
    verified: bool = Field(
        default=False,
        description="Whether the knowledge is verified"
    )

    @field_validator("title", "problem", "solution")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip leading/trailing whitespace."""
        return v.strip() if v else v

    @field_validator("context")
    @classmethod
    def validate_context(cls, v: Any) -> dict:
        """Ensure context is a dict."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return {}
        return v if isinstance(v, dict) else {}

    @model_validator(mode="after")
    def update_timestamp(self) -> "KnowledgeUnit":
        """Auto-update updated_at on modification."""
        # Only set if not explicitly provided (for updates)
        if hasattr(self, "_updating"):
            self.updated_at = datetime.utcnow()
        return self

    def get_tags(self) -> list[str]:
        """Get tags from context."""
        return self.context.get("tags", [])

    def add_tag(self, tag: str) -> None:
        """Add a tag to the context."""
        if "tags" not in self.context:
            self.context["tags"] = []
        if tag not in self.context["tags"]:
            self.context["tags"].append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the context."""
        if "tags" in self.context and tag in self.context["tags"]:
            self.context["tags"].remove(tag)

    def increment_usage(self) -> None:
        """Increment usage count."""
        self.usage_count += 1

    def mark_as_verified(self) -> None:
        """Mark knowledge as verified."""
        self.verified = True

    def to_db_dict(self) -> dict:
        """Convert to database-friendly dict."""
        return {
            "id": self.id,
            "title": self.title,
            "problem": self.problem,
            "solution": self.solution,
            "context": json.dumps(self.context),
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "source": self.source.value,
            "verified": 1 if self.verified else 0,
        }

    @classmethod
    def from_db_dict(cls, data: dict) -> "KnowledgeUnit":
        """Create from database dict."""
        context = data.get("context", "{}")
        if isinstance(context, str):
            context = json.loads(context)

        return cls(
            id=data["id"],
            title=data["title"],
            problem=data["problem"],
            solution=data["solution"],
            context=context,
            confidence=data.get("confidence", 0.5),
            usage_count=data.get("usage_count", 0),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            source=Source(data.get("source", "manual")),
            verified=bool(data.get("verified", 0)),
        )


class Feedback(BaseModel):
    """User feedback on knowledge units."""

    id: str = Field(
        default_factory=lambda: f"fb_{secrets.token_hex(4)}",
        description="Unique identifier"
    )
    ku_id: str = Field(..., description="Knowledge unit ID")
    helpful: bool = Field(..., description="Whether the feedback was helpful")
    feedback_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Feedback timestamp"
    )
    source: str | None = Field(
        default=None,
        description="Feedback source"
    )

    def to_db_dict(self) -> dict:
        """Convert to database-friendly dict."""
        return {
            "id": self.id,
            "ku_id": self.ku_id,
            "helpful": 1 if self.helpful else 0,
            "feedback_at": self.feedback_at.isoformat(),
            "source": self.source,
        }

    @classmethod
    def from_db_dict(cls, data: dict) -> "Feedback":
        """Create from database dict."""
        return cls(
            id=data["id"],
            ku_id=data["ku_id"],
            helpful=bool(data.get("helpful", 0)),
            feedback_at=datetime.fromisoformat(data["feedback_at"]),
            source=data.get("source"),
        )


class SearchResult(BaseModel):
    """Full-text search result."""

    knowledge: KnowledgeUnit
    rank: float = Field(..., description="FTS5 rank score")
    matched_text: str | None = Field(
        default=None,
        description="Matched text snippet"
    )


class ListFilter(BaseModel):
    """Filters for listing knowledge units."""

    tags: list[str] | None = None
    source: Source | None = None
    verified: bool | None = None
    min_confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0
    )
    max_confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0
    )
    created_after: datetime | None = None
    created_before: datetime | None = None
    updated_after: datetime | None = None
    updated_before: datetime | None = None
