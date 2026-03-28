# Tests for Database Module

"""Basic tests for database functionality."""

import pytest
import tempfile
from pathlib import Path

from cq.core.models import KnowledgeUnit, Source, Feedback
from cq.core.storage import Database
from cq.repositories.knowledge import KnowledgeRepository
from cq.repositories.feedback import FeedbackRepository


@pytest.fixture
async def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    db = Database(db_path)
    # initialize() will run migrations automatically
    await db.initialize()

    yield db

    await db.close()
    # Clean up
    if db_path.exists():
        db_path.unlink()


@pytest.mark.asyncio
async def test_database_initialize(temp_db: Database):
    """Test database initialization."""
    version = await temp_db.get_version()
    assert version >= 0


@pytest.mark.asyncio
async def test_knowledge_repository_create(temp_db: Database):
    """Test creating a knowledge unit."""
    repo = KnowledgeRepository(temp_db)

    ku = KnowledgeUnit(
        title="Test Knowledge",
        problem="How to test?",
        solution="Use pytest!",
        context={"tags": ["testing", "python"]},
        source=Source.CLAUDE_CODE,
    )

    created = await repo.create(ku)

    assert created.id == ku.id
    assert created.title == "Test Knowledge"
    assert created.problem == "How to test?"
    assert "testing" in created.get_tags()


@pytest.mark.asyncio
async def test_knowledge_repository_get(temp_db: Database):
    """Test getting a knowledge unit by ID."""
    repo = KnowledgeRepository(temp_db)

    ku = KnowledgeUnit(
        title="Get Test",
        problem="Find me",
        solution="Found!",
    )

    await repo.create(ku)

    found = await repo.get(ku.id)
    assert found is not None
    assert found.id == ku.id
    assert found.title == "Get Test"


@pytest.mark.asyncio
async def test_knowledge_repository_search(temp_db: Database):
    """Test full-text search."""
    repo = KnowledgeRepository(temp_db)

    await repo.create(KnowledgeUnit(
        title="React Hooks Tutorial",
        problem="How to use useState?",
        solution="const [count, setCount] = useState(0)",
        context={"tags": ["react", "hooks"]},
    ))

    await repo.create(KnowledgeUnit(
        title="Python Async",
        problem="How to use async/await?",
        solution="async def foo(): await bar()",
        context={"tags": ["python", "async"]},
    ))

    # Search for React
    results = await repo.search("React")
    assert len(results) > 0
    assert "React" in results[0].knowledge.title

    # Search with tag filter
    results = await repo.search("use", tags=["react"])
    assert len(results) > 0


@pytest.mark.asyncio
async def test_knowledge_repository_update(temp_db: Database):
    """Test updating a knowledge unit."""
    repo = KnowledgeRepository(temp_db)

    ku = await repo.create(KnowledgeUnit(
        title="Update Test",
        problem="Old problem",
        solution="Old solution",
        confidence=0.5,
    ))

    updated = await repo.update(ku.id, {
        "confidence": 0.9,
        "verified": True,
    })

    assert updated.confidence == 0.9
    assert updated.verified is True


@pytest.mark.asyncio
async def test_knowledge_repository_increment_usage(temp_db: Database):
    """Test incrementing usage count."""
    repo = KnowledgeRepository(temp_db)

    ku = await repo.create(KnowledgeUnit(
        title="Usage Test",
        problem="Test",
        solution="Solution",
    ))

    assert ku.usage_count == 0

    updated = await repo.increment_usage(ku.id)
    assert updated.usage_count == 1

    updated = await repo.increment_usage(ku.id)
    assert updated.usage_count == 2


@pytest.mark.asyncio
async def test_knowledge_repository_list_with_filters(temp_db: Database):
    """Test listing knowledge units with filters."""
    repo = KnowledgeRepository(temp_db)

    await repo.create(KnowledgeUnit(
        title="High Confidence",
        problem="Test",
        solution="Solution",
        confidence=0.9,
        verified=True,
    ))

    await repo.create(KnowledgeUnit(
        title="Low Confidence",
        problem="Test",
        solution="Solution",
        confidence=0.2,
    ))

    # Filter by min confidence
    from cq.core.models import ListFilter
    results = await repo.list(
        filters=ListFilter(min_confidence=0.5)
    )
    assert len(results) == 1
    assert results[0].confidence >= 0.5

    # Filter by verified
    results = await repo.list(
        filters=ListFilter(verified=True)
    )
    assert len(results) == 1
    assert results[0].verified is True


@pytest.mark.asyncio
async def test_knowledge_repository_delete(temp_db: Database):
    """Test deleting a knowledge unit."""
    repo = KnowledgeRepository(temp_db)

    ku = await repo.create(KnowledgeUnit(
        title="Delete Test",
        problem="Test",
        solution="Solution",
    ))

    assert await repo.get(ku.id) is not None

    result = await repo.delete(ku.id)
    assert result is True

    assert await repo.get(ku.id) is None


@pytest.mark.asyncio
async def test_feedback_repository(temp_db: Database):
    """Test feedback repository."""
    ku_repo = KnowledgeRepository(temp_db)
    fb_repo = FeedbackRepository(temp_db)

    ku = await ku_repo.create(KnowledgeUnit(
        title="Feedback Test",
        problem="Test",
        solution="Solution",
    ))

    # Create feedback
    fb = await fb_repo.create(Feedback(
        ku_id=ku.id,
        helpful=True,
        source="test",
    ))

    assert fb.id is not None
    assert fb.helpful is True

    # Get feedback by KU ID
    feedbacks = await fb_repo.get_by_ku_id(ku.id)
    assert len(feedbacks) == 1
    assert feedbacks[0].helpful is True

    # Get stats
    stats = await fb_repo.get_feedback_stats(ku.id)
    assert stats["helpful_count"] == 1
    assert stats["total_count"] == 1


@pytest.mark.asyncio
async def test_feedback_stats_helpful_and_not(temp_db: Database):
    """Test feedback statistics with both helpful and not helpful."""
    ku_repo = KnowledgeRepository(temp_db)
    fb_repo = FeedbackRepository(temp_db)

    ku = await ku_repo.create(KnowledgeUnit(
        title="Stats Test",
        problem="Test",
        solution="Solution",
    ))

    await fb_repo.create(Feedback(ku_id=ku.id, helpful=True))
    await fb_repo.create(Feedback(ku_id=ku.id, helpful=True))
    await fb_repo.create(Feedback(ku_id=ku.id, helpful=False))

    stats = await fb_repo.get_feedback_stats(ku.id)
    assert stats["helpful_count"] == 2
    assert stats["not_helpful_count"] == 1
    assert stats["total_count"] == 3
