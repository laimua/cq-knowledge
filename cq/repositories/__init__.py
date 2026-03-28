# Repositories Module

"""Repository pattern for database access."""

from .base import BaseRepository
from .feedback import FeedbackRepository
from .knowledge import KnowledgeRepository

__all__ = [
    "BaseRepository",
    "KnowledgeRepository",
    "FeedbackRepository",
]
