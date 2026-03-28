"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def tmp_db_path(tmp_path):
    """Create a temporary database path for testing."""
    return tmp_path / "test_knowledge.db"
