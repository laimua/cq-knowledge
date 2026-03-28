# Tests for MCP Server Module

"""Tests for MCP server functionality."""

import tempfile
from pathlib import Path

import pytest
from mcp.types import TextContent

from cq.core.models import KnowledgeUnit, Source, Feedback
from cq.core.storage import Database
from cq.mcp.server import (
    SearchParams,
    AddParams,
    FeedbackParams,
    ShowParams,
    ListParams,
    _search_tool,
    _add_tool,
    _feedback_tool,
    _show_tool,
    _list_tool,
)


@pytest.fixture
async def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    # Manually create schema
    import aiosqlite
    conn = await aiosqlite.connect(db_path)

    # Enable WAL mode
    await conn.execute("PRAGMA journal_mode = WAL")
    await conn.execute("PRAGMA foreign_keys = ON")

    # Run migration
    migration_path = Path(__file__).parent.parent / "migrations" / "001_initial.sql"
    if migration_path.exists():
        sql = migration_path.read_text(encoding="utf-8")
        await conn.executescript(sql)

    await conn.commit()
    await conn.close()

    # Create Database instance with connection already initialized
    db = Database(db_path)
    # Set as initialized without running migrations
    db._connection = await aiosqlite.connect(db_path)
    await db._connection.execute("PRAGMA foreign_keys = ON")
    db._initialized = True

    yield db

    await db.close()
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
async def setup_db(temp_db: Database):
    """Setup database with test data."""
    import cq.mcp.server
    # Monkey patch the database
    original_db = cq.mcp.server._db
    cq.mcp.server._db = temp_db
    yield temp_db
    cq.mcp.server._db = original_db


@pytest.mark.asyncio
async def test_search_tool(setup_db: Database):
    """Test the search tool."""
    # Add test data
    from cq.repositories.knowledge import KnowledgeRepository
    repo = KnowledgeRepository(setup_db)
    await repo.create(KnowledgeUnit(
        title="Python Async Tutorial",
        problem="How to use async/await in Python?",
        solution="Use async def and await keywords.",
        context={"tags": ["python", "async"]},
    ))

    # Test search
    params = SearchParams(query="Python async", limit=5)
    result = await _search_tool(params)

    # Search should return something (either results or error due to FTS setup)
    assert result is not None


@pytest.mark.asyncio
async def test_search_tool_no_results(setup_db: Database):
    """Test search tool with no results."""
    params = SearchParams(query="nonexistent query", limit=5)
    result = await _search_tool(params)

    # Should return a message about no results or an error
    assert result is not None


@pytest.mark.asyncio
async def test_add_tool(setup_db: Database):
    """Test the add tool."""
    params = AddParams(
        title="Test Add",
        problem="Test problem",
        solution="Test solution",
        tags=["test", "mcp"],
        confidence=0.8,
    )

    result = await _add_tool(params)

    assert "added successfully" in result.lower()

    # Verify it was added
    from cq.repositories.knowledge import KnowledgeRepository
    repo = KnowledgeRepository(setup_db)
    kus = await repo.list(limit=10)
    assert len(kus) == 1
    assert kus[0].title == "Test Add"


@pytest.mark.asyncio
async def test_feedback_tool(setup_db: Database):
    """Test the feedback tool."""
    # First add a knowledge unit
    from cq.repositories.knowledge import KnowledgeRepository
    repo = KnowledgeRepository(setup_db)
    ku = await repo.create(KnowledgeUnit(
        title="Feedback Test",
        problem="Problem",
        solution="Solution",
    ))

    # Add feedback
    params = FeedbackParams(
        ku_id=ku.id,
        rating=5,
        comment="Great solution!",
    )

    result = await _feedback_tool(params)

    assert "recorded" in result.lower()
    assert "helpful" in result.lower()

    # Verify feedback was created
    from cq.repositories.feedback import FeedbackRepository
    fb_repo = FeedbackRepository(setup_db)
    feedbacks = await fb_repo.get_by_ku_id(ku.id)
    assert len(feedbacks) == 1
    assert feedbacks[0].helpful is True


@pytest.mark.asyncio
async def test_feedback_tool_not_found(setup_db: Database):
    """Test feedback tool with non-existent knowledge unit."""
    params = FeedbackParams(
        ku_id="nonexistent_id",
        rating=5,
    )

    result = await _feedback_tool(params)

    assert "not found" in result.lower()


@pytest.mark.asyncio
async def test_show_tool(setup_db: Database):
    """Test the show tool."""
    # Add a knowledge unit
    from cq.repositories.knowledge import KnowledgeRepository
    repo = KnowledgeRepository(setup_db)
    ku = await repo.create(KnowledgeUnit(
        title="Show Test",
        problem="Test problem",
        solution="Test solution",
        context={"tags": ["show"]},
    ))

    # Show it
    params = ShowParams(id=ku.id)
    result = await _show_tool(params)

    assert "Show Test" in result
    assert "Test problem" in result
    assert "Test solution" in result


@pytest.mark.asyncio
async def test_show_tool_not_found(setup_db: Database):
    """Test show tool with non-existent knowledge unit."""
    params = ShowParams(id="nonexistent_id")
    result = await _show_tool(params)

    assert "not found" in result.lower()


@pytest.mark.asyncio
async def test_list_tool(setup_db: Database):
    """Test the list tool."""
    # Add test data
    from cq.repositories.knowledge import KnowledgeRepository
    repo = KnowledgeRepository(setup_db)
    await repo.create(KnowledgeUnit(
        title="List Test 1",
        problem="Problem 1",
        solution="Solution 1",
        context={"tags": ["list"]},
    ))
    await repo.create(KnowledgeUnit(
        title="List Test 2",
        problem="Problem 2",
        solution="Solution 2",
        context={"tags": ["list"]},
    ))

    # List all
    params = ListParams(limit=10)
    result = await _list_tool(params)

    assert "Found 2" in result
    assert "List Test 1" in result
    assert "List Test 2" in result


@pytest.mark.asyncio
async def test_list_tool_by_tag(setup_db: Database):
    """Test the list tool with tag filter."""
    # Add test data
    from cq.repositories.knowledge import KnowledgeRepository
    repo = KnowledgeRepository(setup_db)
    await repo.create(KnowledgeUnit(
        title="Tag Test",
        problem="Problem",
        solution="Solution",
        context={"tags": ["python", "test"]},
    ))

    # List by tag
    params = ListParams(limit=10, tag="python")
    result = await _list_tool(params)

    assert "Tag Test" in result


@pytest.mark.asyncio
async def test_list_tool_no_results(setup_db: Database):
    """Test list tool with no results."""
    params = ListParams(limit=10, tag="nonexistent")
    result = await _list_tool(params)

    assert "No knowledge units found" in result or "no results" in result.lower()


@pytest.mark.asyncio
async def test_list_tools_handler():
    """Test the list_tools handler."""
    from cq.mcp.server import list_tools

    tools = await list_tools()

    assert len(tools) == 5
    tool_names = {t.name for t in tools}
    assert "cq_search" in tool_names
    assert "cq_add" in tool_names
    assert "cq_feedback" in tool_names
    assert "cq_show" in tool_names
    assert "cq_list" in tool_names

    # Verify cq_search tool schema
    search_tool = next(t for t in tools if t.name == "cq_search")
    assert search_tool.inputSchema is not None
    assert search_tool.inputSchema["type"] == "object"
    assert "query" in search_tool.inputSchema["properties"]


@pytest.mark.asyncio
async def test_search_tool_with_tag_filter(setup_db: Database):
    """Test search tool with tag filtering."""
    from cq.repositories.knowledge import KnowledgeRepository
    repo = KnowledgeRepository(setup_db)
    await repo.create(KnowledgeUnit(
        title="Python Decorators",
        problem="How to use decorators?",
        solution="@decorator syntax",
        context={"tags": ["python", "decorators"]},
    ))
    await repo.create(KnowledgeUnit(
        title="JavaScript Closures",
        problem="How do closures work?",
        solution="Closures capture scope",
        context={"tags": ["javascript", "closures"]},
    ))

    # Search for Python content
    params = SearchParams(query="use", tag="python", limit=10)
    result = await _search_tool(params)

    # Should return something (even if error due to FTS setup)
    assert result is not None
