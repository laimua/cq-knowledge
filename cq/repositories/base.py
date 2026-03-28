# Base Repository

"""Base repository class with common database operations."""

import builtins
import logging
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from cq.core.models import KnowledgeUnit
from cq.core.storage import Database

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=KnowledgeUnit)


class BaseRepository(ABC, Generic[T]):
    """Base repository with common CRUD operations.

    Provides a foundation for all repositories with standard
    create, read, update, and delete operations.
    """

    def __init__(self, database: Database):
        """Initialize repository.

        Args:
            database: Database instance
        """
        self._db = database

    @property
    def db(self) -> Database:
        """Get database instance."""
        return self._db

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity.

        Args:
            entity: Entity to create

        Returns:
            Created entity with generated ID
        """
        pass

    @abstractmethod
    async def get(self, id: str) -> T | None:
        """Get entity by ID.

        Args:
            id: Entity ID

        Returns:
            Entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def update(self, id: str, data: dict[str, Any]) -> T:
        """Update entity.

        Args:
            id: Entity ID
            data: Fields to update

        Returns:
            Updated entity

        Raises:
            NotFoundError: If entity not found
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete entity.

        Args:
            id: Entity ID

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def list(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[T]:
        """List entities with optional filters.

        Args:
            filters: Optional filter criteria
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of entities
        """
        pass

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count entities with optional filters.

        Args:
            filters: Optional filter criteria

        Returns:
            Number of entities
        """
        raise NotImplementedError("Count not implemented")

    async def exists(self, id: str) -> bool:
        """Check if entity exists.

        Args:
            id: Entity ID

        Returns:
            True if exists, False otherwise
        """
        return await self.get(id) is not None

    async def _build_where_clause(
        self,
        filters: dict[str, Any],
        param_prefix: str = "p"
    ) -> tuple[str, builtins.list[Any]]:
        """Build WHERE clause from filters.

        Args:
            filters: Filter criteria
            param_prefix: Prefix for parameter names

        Returns:
            Tuple of (where_clause, parameters)
        """
        if not filters:
            return "", []

        conditions = []
        params = []

        for key, value in filters.items():
            if value is None:
                continue

            param_name = f"{param_prefix}_{len(params)}"
            conditions.append(f"{key} = :{param_name}")
            params.append(value)

        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        return where_clause, params


class NotFoundError(Exception):
    """Entity not found error."""

    def __init__(self, entity_type: str, id: str):
        self.entity_type = entity_type
        self.id = id
        super().__init__(f"{entity_type} with id '{id}' not found")
