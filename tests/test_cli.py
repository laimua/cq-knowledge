# Tests for CLI Module

"""Tests for CLI functionality."""

import json
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner
from typer.testing import CliRunner as TyperCliRunner

from cq.cli import app
from cq.core.models import KnowledgeUnit, Source
from cq.core.storage import Database
from cq.repositories.knowledge import KnowledgeRepository
from cq.repositories.feedback import FeedbackRepository

# Use Typer's CliRunner for Typer applications
runner = TyperCliRunner()


def _setup_temp_db(db_path: Path) -> None:
    """Setup a temporary database with schema (sync version)."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    
    # Run migration
    migration_path = Path(__file__).parent.parent / "migrations" / "001_initial.sql"
    if migration_path.exists():
        sql = migration_path.read_text(encoding="utf-8")
        conn.executescript(sql)
    
    conn.commit()
    conn.close()


def _add_test_ku(db_path: Path, title: str, problem: str = "Problem", solution: str = "Solution", tags: list = None) -> str:
    """Add a test knowledge unit (sync version)."""
    import sqlite3
    import uuid
    from datetime import datetime
    
    ku_id = str(uuid.uuid4())
    conn = sqlite3.connect(db_path)
    
    context = {"tags": tags or []}
    conn.execute(
        """INSERT INTO knowledge_units (id, title, problem, solution, context, confidence, source)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (ku_id, title, problem, solution, json.dumps(context), 0.5, "manual")
    )
    conn.commit()
    conn.close()
    return ku_id


@pytest.fixture
def temp_db_path(tmp_path):
    """Create a temporary database path for testing."""
    db_path = tmp_path / "test_knowledge.db"
    _setup_temp_db(db_path)
    return db_path


class TestCLI:
    """CLI tests - run synchronously (no pytest.mark.asyncio)."""

    def _clear_global_db(self):
        """Clear the global database instance before each test."""
        from cq.core import storage
        storage._db_instance = None

    def test_cli_add_command(self, temp_db_path: Path, monkeypatch):
        """Test the CLI add command."""
        self._clear_global_db()

        # Monkey patch the default db path
        from cq import core
        monkeypatch.setattr(core.storage, "DEFAULT_DB_PATH", temp_db_path)

        result = runner.invoke(app, [
            "add",
            "--title", "Test CLI Add",
            "--problem", "Test problem",
            "--solution", "Test solution",
            "--tags", "test,cli",
        ])

        assert result.exit_code == 0, f"Output: {result.stdout}"

    def test_cli_list_command(self, temp_db_path: Path, monkeypatch):
        """Test the CLI list command."""
        self._clear_global_db()

        # Add test data
        _add_test_ku(temp_db_path, "List Test 1", tags=["test"])

        from cq import core
        monkeypatch.setattr(core.storage, "DEFAULT_DB_PATH", temp_db_path)

        result = runner.invoke(app, ["list", "--limit", "10"])

        assert result.exit_code == 0, f"Output: {result.stdout}"

    def test_cli_search_command(self, temp_db_path: Path, monkeypatch):
        """Test the CLI search command."""
        # Add test data
        _add_test_ku(temp_db_path, "Search Target", "Search problem description", "Search solution")

        from cq import core
        monkeypatch.setattr(core.storage, "DEFAULT_DB_PATH", temp_db_path)

        result = runner.invoke(app, ["search", "Search"])

        # Search command should run
        assert result is not None

    def test_cli_show_command(self, temp_db_path: Path, monkeypatch):
        """Test the CLI show command."""
        self._clear_global_db()

        # Add test data
        ku_id = _add_test_ku(temp_db_path, "Show Test")

        from cq import core
        monkeypatch.setattr(core.storage, "DEFAULT_DB_PATH", temp_db_path)

        result = runner.invoke(app, ["show", ku_id])

        assert result.exit_code == 0, f"Output: {result.stdout}"
        assert "Show Test" in result.stdout

    def test_cli_delete_command(self, temp_db_path: Path, monkeypatch):
        """Test the CLI delete command."""
        self._clear_global_db()

        # Add test data
        ku_id = _add_test_ku(temp_db_path, "Delete Test")

        from cq import core
        monkeypatch.setattr(core.storage, "DEFAULT_DB_PATH", temp_db_path)

        # Delete with force flag (simulate user input 'y' for confirmation)
        result = runner.invoke(app, ["delete", ku_id, "--force"], input="y")

        assert result.exit_code == 0, f"Output: {result.stdout}"

    def test_cli_export_command(self, temp_db_path: Path, monkeypatch, tmp_path):
        """Test the CLI export command."""
        self._clear_global_db()

        # Add test data
        _add_test_ku(temp_db_path, "Export Test", tags=["export"])

        from cq import core
        monkeypatch.setattr(core.storage, "DEFAULT_DB_PATH", temp_db_path)

        output_file = tmp_path / "export.json"
        result = runner.invoke(app, ["export", "--output", str(output_file)])

        assert result.exit_code == 0, f"Output: {result.stdout}"
        assert output_file.exists()

        # Verify export content
        with output_file.open("r") as f:
            data = json.load(f)
        assert "knowledge_units" in data
        assert len(data["knowledge_units"]) >= 1

    def test_cli_feedback_command(self, temp_db_path: Path, monkeypatch):
        """Test the CLI feedback command."""
        self._clear_global_db()

        # Add test data
        ku_id = _add_test_ku(temp_db_path, "Feedback Test")

        from cq import core
        monkeypatch.setattr(core.storage, "DEFAULT_DB_PATH", temp_db_path)

        result = runner.invoke(app, [
            "feedback", ku_id,
            "--rating", "5",
            "--comment", "Great solution!",
        ])

        assert result.exit_code == 0, f"Output: {result.stdout}"

    def test_cli_import_command(self, temp_db_path: Path, monkeypatch, tmp_path):
        """Test the CLI import command."""
        # Create export file
        export_file = tmp_path / "import.json"
        export_data = {
            "knowledge_units": [
                {
                    "id": "ku_import_test",
                    "title": "Import Test",
                    "problem": "Import problem",
                    "solution": "Import solution",
                    "context": {"tags": ["import"]},
                    "confidence": 0.8,
                    "usage_count": 0,
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00",
                    "source": "manual",
                    "verified": False,
                }
            ],
            "feedback_history": [],
        }

        with export_file.open("w") as f:
            json.dump(export_data, f)

        from cq import core
        monkeypatch.setattr(core.storage, "DEFAULT_DB_PATH", temp_db_path)

        result = runner.invoke(app, ["import-cmd", "--input", str(export_file)])

        assert result.exit_code == 0, f"Output: {result.stdout}"
