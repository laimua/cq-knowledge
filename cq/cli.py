# CLI Entry Point

"""Command-line interface for Cq."""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cq import __version__
from cq.core.models import Feedback, KnowledgeUnit, Source
from cq.core.scoring import calculate_confidence
from cq.core.storage import Database, get_database, close_database
from cq.repositories.feedback import FeedbackRepository
from cq.repositories.knowledge import KnowledgeRepository

# Fix GBK encoding on Windows - Rich uses Unicode chars (✓, ✗) that crash in GBK terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

app = typer.Typer(
    name="cq",
    help="Stack Overflow for AI Coding Agents - Knowledge sharing platform",
    add_completion=False,
)
console = Console()


def get_db() -> Database:
    """Get or create database instance (sync wrapper)."""
    async def _get():
        return await get_database()
    return asyncio.run(_run_async(_get()))


async def _init_db() -> Database:
    """Initialize database."""
    db = await get_database()
    return db


async def _run_async(coro) -> None:
    """Run an async coroutine and ensure cleanup."""
    try:
        await coro
    finally:
        await close_database()


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"[bold green]Cq[/bold green] version {__version__}")


@app.command()
def init() -> None:
    """Initialize knowledge base."""
    async def _init() -> None:
        console.print("[yellow]Initializing knowledge base...[/yellow]")
        db = await _init_db()
        console.print(f"[green]✓ Knowledge base initialized at {db.db_path}[/green]")

    asyncio.run(_run_async(_init()))


@app.command()
def add(
    title: str = typer.Option(..., "--title", "-t", help="Knowledge title"),
    problem: str = typer.Option(..., "--problem", "-p", help="Problem description"),
    solution: str = typer.Option(..., "--solution", "-s", help="Solution description"),
    tags: str = typer.Option("", "--tags", help="Tags (comma-separated)"),
    confidence: float = typer.Option(0.5, "--confidence", "-c", help="Confidence level (0-1)"),
) -> None:
    """Add a knowledge unit."""
    async def _add() -> None:
        db = await _init_db()
        repo = KnowledgeRepository(db)

        # Parse tags
        tag_list = [t.strip() for t in tags.split(",")] if tags else []

        # Create knowledge unit
        ku = KnowledgeUnit(
            title=title,
            problem=problem,
            solution=solution,
            context={"tags": tag_list} if tag_list else {},
            confidence=confidence,
            source=Source.MANUAL,
        )

        await repo.create(ku)

        console.print(f"[green]✓[/green] Knowledge unit added: [bold cyan]{ku.id}[/bold cyan]")
        console.print(f"  Title: {title}")
        if tag_list:
            console.print(f"  Tags: {', '.join(tag_list)}")

    asyncio.run(_run_async(_add()))


@app.command()
def list(
    limit: int = typer.Option(20, "--limit", "-l", help="Number of results"),
    tag: Optional[str] = typer.Option(None, "--tag", help="Filter by tag"),
    offset: int = typer.Option(0, "--offset", help="Skip first N results"),
) -> None:
    """List knowledge units."""
    async def _list() -> None:
        db = await _init_db()
        repo = KnowledgeRepository(db)

        if tag:
            kus = await repo.get_by_tag(tag, limit=limit)
        else:
            kus = await repo.list(limit=limit, offset=offset)

        if not kus:
            console.print("[yellow]No knowledge units found[/yellow]")
            return

        table = Table(title="Knowledge Units")
        table.add_column("ID", style="cyan")
        table.add_column("Title")
        table.add_column("Tags", style="green")
        table.add_column("Confidence", justify="right")
        table.add_column("Updated", style="dim")

        for ku in kus:
            tags = ", ".join(ku.get_tags())
            table.add_row(
                ku.id[:12],
                ku.title[:40] + "..." if len(ku.title) > 40 else ku.title,
                tags[:20] + "..." if len(tags) > 20 else tags,
                f"{ku.confidence:.1f}",
                ku.updated_at.strftime("%Y-%m-%d") if ku.updated_at else "",
            )

        console.print(table)

    asyncio.run(_run_async(_list()))


@app.command()
def search(
    query: str = typer.Argument(help="Search query"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results"),
    tag: Optional[str] = typer.Option(None, "--tag", help="Filter by tag"),
) -> None:
    """Search knowledge units using FTS5."""
    async def _search() -> None:
        db = await _init_db()
        repo = KnowledgeRepository(db)

        tags = [tag] if tag else None
        results = await repo.search(query, tags=tags, limit=limit)

        if not results:
            console.print(f"[yellow]No results found for '{query}'[/yellow]")
            return

        console.print(f"\n[bold]Found {len(results)} results for '{query}'[/bold]\n")

        for result in results:
            ku = result.knowledge
            tags_str = ", ".join(ku.get_tags())

            console.print(Panel(
                f"[cyan]Title:[/cyan] {ku.title}\n"
                f"[dim]ID: {ku.id}[/dim]\n"
                f"[green]Tags:[/green] {tags_str if tags_str else 'none'}\n"
                f"[yellow]Rank:[/yellow] {result.rank:.2f} | "
                f"[yellow]Confidence:[/yellow] {ku.confidence:.1f}\n"
                f"\n[cyan]Problem:[/cyan]\n{ku.problem[:200]}{'...' if len(ku.problem) > 200 else ''}\n"
                f"\n[cyan]Solution:[/cyan]\n{ku.solution[:200]}{'...' if len(ku.solution) > 200 else ''}",
                title=f"[bold]{ku.id[:12]}[/bold]",
                border_style="blue" if ku.verified else "dim",
            ))

    asyncio.run(_run_async(_search()))


@app.command()
def show(
    id: str = typer.Argument(help="Knowledge unit ID"),
) -> None:
    """Show knowledge unit details."""
    async def _show() -> None:
        db = await _init_db()
        repo = KnowledgeRepository(db)

        ku = await repo.get(id)

        if ku is None:
            console.print(f"[red]✗[/red] Knowledge unit '{id}' not found")
            raise typer.Exit(1)

        tags_str = ", ".join(ku.get_tags())

        console.print(Panel(
            f"[cyan]Title:[/cyan] {ku.title}\n"
            f"[dim]ID: {ku.id}[/dim]\n"
            f"[dim]Created: {ku.created_at.strftime('%Y-%m-%d %H:%M')}[/dim]\n"
            f"[dim]Updated: {ku.updated_at.strftime('%Y-%m-%d %H:%M')}[/dim]\n"
            f"[green]Source:[/green] {ku.value if hasattr(ku, 'value') else ku.source}\n"
            f"[green]Verified:[/green] {'Yes' if ku.verified else 'No'}\n"
            f"[green]Confidence:[/green] {ku.confidence:.2f}\n"
            f"[green]Usage Count:[/green] {ku.usage_count}\n"
            f"[green]Tags:[/green] {tags_str if tags_str else 'none'}\n"
            f"\n[bold yellow]Problem:[/bold yellow]\n{ku.problem}\n"
            f"\n[bold green]Solution:[/bold green]\n{ku.solution}",
            title="[bold]Knowledge Unit Details[/bold]",
            border_style="green" if ku.verified else "blue",
        ))

        # Show feedback stats if any
        feedback_repo = FeedbackRepository(db)
        stats = await feedback_repo.get_feedback_stats(ku.id)
        if stats["total_count"] > 0:
            console.print(f"\n[dim]Feedback: {stats['helpful_count']} helpful, "
                        f"{stats['not_helpful_count']} not helpful[/dim]")

    asyncio.run(_run_async(_show()))


@app.command()
def delete(
    id: str = typer.Argument(help="Knowledge unit ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Force delete without confirmation"),
) -> None:
    """Delete a knowledge unit."""
    async def _delete() -> None:
        db = await _init_db()
        repo = KnowledgeRepository(db)

        # Check if exists
        ku = await repo.get(id)
        if ku is None:
            console.print(f"[red]✗[/red] Knowledge unit '{id}' not found")
            raise typer.Exit(1)

        # Confirm deletion
        if not force:
            console.print("[yellow]Deleting knowledge unit:[/yellow]")
            console.print(f"  ID: {ku.id}")
            console.print(f"  Title: {ku.title}")
            confirm = typer.confirm("Are you sure?")
            if not confirm:
                console.print("[dim]Cancelled[/dim]")
                raise typer.Exit()

        # Delete
        success = await repo.delete(id)

        if success:
            console.print(f"[green]✓[/green] Knowledge unit '{id}' deleted")
        else:
            console.print(f"[red]✗[/red] Failed to delete knowledge unit '{id}'")
            raise typer.Exit(1)

    asyncio.run(_run_async(_delete()))


@app.command()
def export(
    output: str = typer.Option("backup.json", "--output", "-o", help="Output file path"),
    include_feedback: bool = typer.Option(False, "--feedback", "-f", help="Include feedback data"),
) -> None:
    """Export knowledge base to JSON."""
    async def _export() -> None:
        db = await _init_db()
        repo = KnowledgeRepository(db)
        feedback_repo = FeedbackRepository(db)

        # Get all knowledge units
        kus = await repo.list(limit=10000)

        export_data = {
            "exported_at": datetime.utcnow().isoformat(),
            "knowledge_units": [],
            "feedback_history": [] if include_feedback else None,
        }

        for ku in kus:
            ku_data = {
                "id": ku.id,
                "title": ku.title,
                "problem": ku.problem,
                "solution": ku.solution,
                "context": ku.context,
                "confidence": ku.confidence,
                "usage_count": ku.usage_count,
                "created_at": ku.created_at.isoformat() if ku.created_at else None,
                "updated_at": ku.updated_at.isoformat() if ku.updated_at else None,
                "source": ku.source.value if isinstance(ku.source, Source) else ku.source,
                "verified": ku.verified,
            }
            export_data["knowledge_units"].append(ku_data)

            # Include feedback if requested
            if include_feedback:
                feedback = await feedback_repo.get_by_ku_id(ku.id, limit=1000)
                for fb in feedback:
                    export_data["feedback_history"].append({
                        "id": fb.id,
                        "ku_id": fb.ku_id,
                        "helpful": fb.helpful,
                        "feedback_at": fb.feedback_at.isoformat() if fb.feedback_at else None,
                        "source": fb.source,
                    })

        # Write to file
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        console.print(f"[green]✓[/green] Exported {len(kus)} knowledge units to {output}")
        if include_feedback:
            console.print(f"  Included {len(export_data['feedback_history'])} feedback records")

    asyncio.run(_run_async(_export()))


@app.command()
def feedback(
    ku_id: str = typer.Argument(help="Knowledge unit ID"),
    rating: int = typer.Option(..., "--rating", "-r", min=1, max=5, help="Rating (1-5)"),
    comment: str = typer.Option("", "--comment", "-c", help="Optional comment"),
) -> None:
    """Add feedback for a knowledge unit."""
    async def _feedback() -> None:
        db = await _init_db()
        ku_repo = KnowledgeRepository(db)
        feedback_repo = FeedbackRepository(db, ku_repo=ku_repo)

        # Check if knowledge unit exists
        ku = await ku_repo.get(ku_id)
        if ku is None:
            console.print(f"[red]✗[/red] Knowledge unit '{ku_id}' not found")
            raise typer.Exit(1)

        # Create feedback (rating >= 4 is considered helpful)
        feedback = Feedback(
            ku_id=ku_id,
            helpful=rating >= 4,
            source=comment or None,
        )

        await feedback_repo.create(feedback)

        helpful_str = "[green]helpful[/green]" if feedback.helpful else "[red]not helpful[/red]"
        console.print(f"[green]✓[/green] Feedback recorded as {helpful_str}")
        console.print(f"  Rating: {rating}/5")
        if comment:
            console.print(f"  Comment: {comment}")

    asyncio.run(_run_async(_feedback()))


@app.command()
def import_cmd(
    input: str = typer.Option(..., "--input", "-i", help="Input JSON file path"),
    skip_existing: bool = typer.Option(False, "--skip-existing", "-s", help="Skip if already exists"),
    recalculate: bool = typer.Option(False, "--recalculate", "-r", help="Recalculate confidence after import"),
) -> None:
    """Import knowledge base from JSON."""
    async def _import() -> None:
        db = await _init_db()
        ku_repo = KnowledgeRepository(db)
        # Only pass ku_repo if we want to recalculate confidence during import
        feedback_repo = FeedbackRepository(db, ku_repo=ku_repo if recalculate else None)

        input_path = Path(input)
        if not input_path.exists():
            console.print(f"[red]✗[/red] File not found: {input}")
            raise typer.Exit(1)

        # Read and parse JSON
        with input_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        imported = 0
        skipped = 0

        # Import knowledge units
        for ku_data in data.get("knowledge_units", []):
            ku_id = ku_data["id"]

            # Check if exists
            if skip_existing and await ku_repo.exists(ku_id):
                skipped += 1
                continue

            ku = KnowledgeUnit(
                id=ku_id,
                title=ku_data["title"],
                problem=ku_data["problem"],
                solution=ku_data["solution"],
                context=ku_data.get("context", {}),
                confidence=ku_data.get("confidence", 0.5),
                usage_count=ku_data.get("usage_count", 0),
                created_at=datetime.fromisoformat(ku_data["created_at"]) if ku_data.get("created_at") else None,
                updated_at=datetime.fromisoformat(ku_data["updated_at"]) if ku_data.get("updated_at") else None,
                source=Source(ku_data.get("source", "manual")),
                verified=ku_data.get("verified", False),
            )
            await ku_repo.create(ku)
            imported += 1

        # Import feedback if available
        feedback_count = 0
        for fb_data in data.get("feedback_history", []):
            try:
                feedback = Feedback(
                    id=fb_data["id"],
                    ku_id=fb_data["ku_id"],
                    helpful=fb_data["helpful"],
                    feedback_at=datetime.fromisoformat(fb_data["feedback_at"]) if fb_data.get("feedback_at") else None,
                    source=fb_data.get("source"),
                )
                await feedback_repo.create(feedback)
                feedback_count += 1
            except Exception:
                pass  # Skip invalid feedback

        console.print("[green]✓[/green] Import complete:")
        console.print(f"  Imported: {imported} knowledge units")
        if skipped > 0:
            console.print(f"  Skipped: {skipped} existing units")
        if feedback_count > 0:
            console.print(f"  Feedback: {feedback_count} records")

    # Use a different name to avoid conflict with import built-in
    asyncio.run(_run_async(_import()))


@app.command()
def recalculate(
    ku_id: str = typer.Option(None, "--id", "-i", help="Specific knowledge unit ID to recalculate"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Show changes without applying"),
) -> None:
    """Recalculate confidence scores for knowledge units."""
    async def _recalculate() -> None:
        db = await _init_db()
        ku_repo = KnowledgeRepository(db)
        feedback_repo = FeedbackRepository(db, ku_repo=ku_repo)

        if ku_id:
            # Recalculate single knowledge unit
            ku = await ku_repo.get(ku_id)
            if ku is None:
                console.print(f"[red]✗[/red] Knowledge unit '{ku_id}' not found")
                raise typer.Exit(1)

            kus = [ku]
        else:
            # Get all knowledge units
            kus = await ku_repo.list(limit=10000)

        if not kus:
            console.print("[yellow]No knowledge units found[/yellow]")
            return

        console.print(f"[bold]Recalculating confidence for {len(kus)} knowledge unit(s)[/bold]\n")

        table = Table(title="Confidence Updates")
        table.add_column("ID", style="cyan")
        table.add_column("Title")
        table.add_column("Old", justify="right", style="yellow")
        table.add_column("New", justify="right", style="green")
        table.add_column("Change", justify="right")
        table.add_column("Feedback", style="dim")

        updated_count = 0

        for ku in kus:
            # Get feedback stats
            stats = await feedback_repo.get_feedback_stats(ku.id)

            # Calculate new confidence
            new_confidence = calculate_confidence(
                helpful_count=stats["helpful_count"],
                not_helpful_count=stats["not_helpful_count"],
            )

            old_confidence = ku.confidence
            confidence_diff = new_confidence - old_confidence

            # Skip if no change
            if abs(confidence_diff) < 0.001:
                continue

            # Update confidence (unless dry run)
            if not dry_run:
                await ku_repo.update(ku.id, {"confidence": new_confidence})

            updated_count += 1

            # Format change indicator
            change_str = f"{confidence_diff:+.3f}"
            change_style = "green" if confidence_diff > 0 else "red" if confidence_diff < 0 else "dim"

            # Format feedback summary
            feedback_str = f"+{stats['helpful_count']}/-{stats['not_helpful_count']}"

            table.add_row(
                ku.id[:12],
                ku.title[:30] + "..." if len(ku.title) > 30 else ku.title,
                f"{old_confidence:.3f}",
                f"{new_confidence:.3f}",
                f"[{change_style}]{change_str}[/{change_style}]",
                feedback_str,
            )

        if updated_count > 0:
            console.print(table)
        else:
            console.print("[dim]No confidence changes needed[/dim]")

        if dry_run:
            console.print(f"\n[yellow]Dry run: {updated_count} update(s) would be applied[/yellow]")
        else:
            console.print(f"\n[green]✓[/green] Updated confidence for {updated_count} knowledge unit(s)")

    asyncio.run(_run_async(_recalculate()))


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
) -> None:
    """Start the web API server."""
    import uvicorn
    from cq.api.app import create_app

    async def start_server() -> None:
        """Start the uvicorn server."""
        app_instance = await create_app()
        uvicorn.run(
            app_instance,
            host=host,
            port=port,
            reload=reload,
        )

    asyncio.run(start_server())


if __name__ == "__main__":
    app()
