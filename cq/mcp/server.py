# MCP Server

"""MCP server implementation for Claude Code integration."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import EmbeddedResource, ImageContent, TextContent, Tool
from pydantic import BaseModel

from cq.core.models import Feedback, KnowledgeUnit, Source
from cq.core.storage import Database, get_database
from cq.repositories.feedback import FeedbackRepository
from cq.repositories.knowledge import KnowledgeRepository

logger = logging.getLogger(__name__)

# Global MCP server instance
server = Server("cq-knowledge")

# Global database instance
_db: Database | None = None


async def get_db() -> Database:
    """Get or create database instance."""
    global _db
    if _db is None:
        _db = await get_database()
    return _db


class SearchParams(BaseModel):
    """Parameters for search tool."""

    query: str
    limit: int = 5
    tag: str | None = None


class AddParams(BaseModel):
    """Parameters for add tool."""

    title: str
    problem: str
    solution: str
    tags: list[str] | None = None
    confidence: float = 0.5


class FeedbackParams(BaseModel):
    """Parameters for feedback tool."""

    ku_id: str
    rating: int  # 1-5
    comment: str | None = None


class ShowParams(BaseModel):
    """Parameters for show tool."""

    id: str


class ListParams(BaseModel):
    """Parameters for list tool."""

    limit: int = 20
    tag: str | None = None


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="cq_search",
            description="Search the knowledge base for solutions to coding problems. Uses full-text search to find relevant knowledge units by title, problem description, and solution.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query - use keywords related to the problem"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results to return (default: 5)",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 50
                    },
                    "tag": {
                        "type": "string",
                        "description": "Filter results by tag (optional)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="cq_add",
            description="Add a new knowledge unit to the knowledge base. Use this to document solutions to coding problems for future reference.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Concise title describing the problem/solution"
                    },
                    "problem": {
                        "type": "string",
                        "description": "Detailed description of the problem"
                    },
                    "solution": {
                        "type": "string",
                        "description": "Detailed solution or fix"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for categorization (e.g., ['python', 'asyncio', 'error'])"
                    },
                    "confidence": {
                        "type": "number",
                        "description": "Confidence level in this solution (0.0-1.0, default: 0.5)",
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "default": 0.5
                    }
                },
                "required": ["title", "problem", "solution"]
            }
        ),
        Tool(
            name="cq_feedback",
            description="Submit feedback on a knowledge unit to help improve the knowledge base quality. Ratings of 4-5 are considered helpful, 1-3 are not helpful.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ku_id": {
                        "type": "string",
                        "description": "Knowledge unit ID to provide feedback on"
                    },
                    "rating": {
                        "type": "number",
                        "description": "Rating from 1-5 (4-5 = helpful, 1-3 = not helpful)",
                        "minimum": 1,
                        "maximum": 5
                    },
                    "comment": {
                        "type": "string",
                        "description": "Optional comment explaining the feedback"
                    }
                },
                "required": ["ku_id", "rating"]
            }
        ),
        Tool(
            name="cq_show",
            description="Get detailed information about a specific knowledge unit by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Knowledge unit ID"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="cq_list",
            description="List knowledge units with optional filtering by tag.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results (default: 20)",
                        "default": 20,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "tag": {
                        "type": "string",
                        "description": "Filter by tag (optional)"
                    }
                },
                "required": []
            }
        ),
    ]


async def _search_tool(params: SearchParams) -> str:
    """Execute search tool."""
    try:
        db = await get_db()
        repo = KnowledgeRepository(db)

        tags = [params.tag] if params.tag else None
        results = await repo.search(params.query, tags=tags, limit=params.limit)

        if not results:
            return f"No results found for query: {params.query}"

        output = [f"Found {len(results)} results for '{params.query}':\n"]

        for i, result in enumerate(results, 1):
            ku = result.knowledge
            tags_str = ", ".join(ku.get_tags()) if ku.get_tags() else "none"
            verified_badge = " ✓" if ku.verified else ""

            output.append(f"""
## {i}. {ku.title}{verified_badge}
**ID:** {ku.id}
**Tags:** {tags_str}
**Confidence:** {ku.confidence:.2f} | **Rank:** {result.rank:.2f}

**Problem:**
{ku.problem[:300]}{'...' if len(ku.problem) > 300 else ''}

**Solution:**
{ku.solution[:500]}{'...' if len(ku.solution) > 500 else ''}

---
""")

        # Increment usage for all found units
        for result in results:
            await repo.increment_usage(result.knowledge.id)

        return "\n".join(output)

    except Exception as e:
        logger.error(f"Error in search_tool: {e}")
        return f"Error searching knowledge base: {e}"


async def _add_tool(params: AddParams) -> str:
    """Execute add tool."""
    try:
        db = await get_db()
        repo = KnowledgeRepository(db)

        ku = KnowledgeUnit(
            title=params.title,
            problem=params.problem,
            solution=params.solution,
            context={"tags": params.tags or []},
            confidence=params.confidence,
            source=Source.CLAUDE_CODE,
        )

        await repo.create(ku)

        return f"✓ Knowledge unit added successfully\n\n**ID:** {ku.id}\n**Title:** {params.title}"

    except Exception as e:
        logger.error(f"Error in add_tool: {e}")
        return f"Error adding knowledge unit: {e}"


async def _feedback_tool(params: FeedbackParams) -> str:
    """Execute feedback tool."""
    try:
        db = await get_db()
        ku_repo = KnowledgeRepository(db)
        feedback_repo = FeedbackRepository(db)

        # Verify knowledge unit exists
        ku = await ku_repo.get(params.ku_id)
        if ku is None:
            return f"✗ Knowledge unit '{params.ku_id}' not found"

        # Create feedback (rating >= 4 is helpful)
        feedback = Feedback(
            ku_id=params.ku_id,
            helpful=params.rating >= 4,
            source=params.comment,
        )

        await feedback_repo.create(feedback)

        helpful_str = "helpful" if feedback.helpful else "not helpful"
        return f"✓ Feedback recorded as {helpful_str}\n\n**Knowledge Unit:** {ku.title}\n**Rating:** {params.rating}/5"

    except Exception as e:
        logger.error(f"Error in feedback_tool: {e}")
        return f"Error recording feedback: {e}"


async def _show_tool(params: ShowParams) -> str:
    """Execute show tool."""
    try:
        db = await get_db()
        repo = KnowledgeRepository(db)

        ku = await repo.get(params.id)

        if ku is None:
            return f"✗ Knowledge unit '{params.id}' not found"

        tags_str = ", ".join(ku.get_tags()) if ku.get_tags() else "none"
        verified_badge = " ✓" if ku.verified else ""

        output = f"""# {ku.title}{verified_badge}

**ID:** {ku.id}
**Source:** {ku.source.value}
**Verified:** {'Yes' if ku.verified else 'No'}
**Confidence:** {ku.confidence:.2f}
**Usage Count:** {ku.usage_count}
**Tags:** {tags_str}
**Created:** {ku.created_at.strftime('%Y-%m-%d %H:%M:%S') if ku.created_at else 'N/A'}
**Updated:** {ku.updated_at.strftime('%Y-%m-%d %H:%M:%S') if ku.updated_at else 'N/A'}

## Problem
{ku.problem}

## Solution
{ku.solution}
"""

        # Get feedback stats
        feedback_repo = FeedbackRepository(db)
        stats = await feedback_repo.get_feedback_stats(ku.id)
        if stats["total_count"] > 0:
            output += f"\n---\n\n**Feedback:** {stats['helpful_count']} helpful, {stats['not_helpful_count']} not helpful (total: {stats['total_count']})"

        return output

    except Exception as e:
        logger.error(f"Error in show_tool: {e}")
        return f"Error showing knowledge unit: {e}"


async def _list_tool(params: ListParams) -> str:
    """Execute list tool."""
    try:
        db = await get_db()
        repo = KnowledgeRepository(db)

        if params.tag:
            kus = await repo.get_by_tag(params.tag, limit=params.limit)
        else:
            kus = await repo.list(limit=params.limit)

        if not kus:
            return "No knowledge units found" + (f" with tag '{params.tag}'" if params.tag else "")

        output = [f"Found {len(kus)} knowledge unit(s):\n"]

        for i, ku in enumerate(kus, 1):
            tags_str = ", ".join(ku.get_tags()) if ku.get_tags() else "none"
            verified_badge = " ✓" if ku.verified else ""

            output.append(f"""## {i}. {ku.title}{verified_badge}
**ID:** {ku.id}
**Tags:** {tags_str}
**Confidence:** {ku.confidence:.2f}
**Updated:** {ku.updated_at.strftime('%Y-%m-%d') if ku.updated_at else 'N/A'}
""")

        return "\n".join(output)

    except Exception as e:
        logger.error(f"Error in list_tool: {e}")
        return f"Error listing knowledge units: {e}"


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls from MCP client."""
    logger.info(f"Tool called: {name} with arguments: {arguments}")

    try:
        if name == "cq_search":
            params = SearchParams(**arguments)
            result = await _search_tool(params)
        elif name == "cq_add":
            params = AddParams(**arguments)
            result = await _add_tool(params)
        elif name == "cq_feedback":
            params = FeedbackParams(**arguments)
            result = await _feedback_tool(params)
        elif name == "cq_show":
            params = ShowParams(**arguments)
            result = await _show_tool(params)
        elif name == "cq_list":
            params = ListParams(**arguments)
            result = await _list_tool(params)
        else:
            result = f"Unknown tool: {name}"

        return [TextContent(type="text", text=result)]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(type="text", text=f"Error executing tool '{name}': {e}")]


async def main() -> None:
    """Main entry point for MCP server."""
    # Initialize database
    db = await get_db()
    logger.info(f"Database initialized at: {db.db_path}")

    # Run MCP server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main_sync() -> None:
    """Synchronous entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    main_sync()
