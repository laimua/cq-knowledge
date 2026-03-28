# Knowledge Repository

"""Repository for knowledge units."""

import builtins
import logging
from datetime import datetime
from typing import Any

from cq.core.models import KnowledgeUnit, ListFilter, SearchResult, Source
from cq.core.storage import Database
from cq.repositories.base import BaseRepository, NotFoundError

logger = logging.getLogger(__name__)


class KnowledgeRepository(BaseRepository[KnowledgeUnit]):
    """Repository for knowledge units with FTS5 search."""

    TABLE_NAME = "knowledge_units"
    FTS_TABLE = "ku_fts"

    def __init__(self, database: Database):
        """Initialize repository.

        Args:
            database: Database instance
        """
        super().__init__(database)

    async def create(self, entity: KnowledgeUnit) -> KnowledgeUnit:
        """Create a new knowledge unit.

        Args:
            entity: Knowledge unit to create

        Returns:
            Created knowledge unit
        """
        data = entity.to_db_dict()
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f":{k}" for k in data.keys()])

        sql = f"""
            INSERT INTO {self.TABLE_NAME} ({columns})
            VALUES ({placeholders})
        """

        await self.db.execute(sql, data)
        logger.debug(f"Created knowledge unit: {entity.id}")

        return entity

    async def create_bulk(self, entities: list[KnowledgeUnit]) -> list[KnowledgeUnit]:
        """Create multiple knowledge units.

        Args:
            entities: List of knowledge units to create

        Returns:
            List of created knowledge units
        """
        if not entities:
            return []

        data_list = [e.to_db_dict() for e in entities]
        columns = ", ".join(data_list[0].keys())
        placeholders = ", ".join([f":{k}" for k in data_list[0].keys()])
        sql = f"""
            INSERT INTO {self.TABLE_NAME} ({columns})
            VALUES ({placeholders})
        """

        params = [tuple(d.values()) for d in data_list]
        await self.db.executemany(sql, params)
        logger.debug(f"Created {len(entities)} knowledge units")

        return entities

    async def get(self, id: str) -> KnowledgeUnit | None:
        """Get knowledge unit by ID.

        Args:
            id: Knowledge unit ID

        Returns:
            Knowledge unit if found, None otherwise
        """
        sql = f"SELECT * FROM {self.TABLE_NAME} WHERE id = :id"
        row = await self.db.fetchone(sql, {"id": id})

        if row is None:
            return None

        return KnowledgeUnit.from_db_dict(row)

    async def get_by_ids(self, ids: list[str]) -> list[KnowledgeUnit]:
        """Get multiple knowledge units by IDs.

        Args:
            ids: List of knowledge unit IDs

        Returns:
            List of found knowledge units
        """
        if not ids:
            return []

        placeholders = ", ".join([f":id{i}" for i in range(len(ids))])
        params = {f"id{i}": id for i, id in enumerate(ids)}

        sql = f"""
            SELECT * FROM {self.TABLE_NAME}
            WHERE id IN ({placeholders})
        """

        rows = await self.db.fetchall(sql, params)
        return [KnowledgeUnit.from_db_dict(row) for row in rows]

    async def update(self, id: str, data: dict[str, Any]) -> KnowledgeUnit:
        """Update knowledge unit.

        Args:
            id: Knowledge unit ID
            data: Fields to update

        Returns:
            Updated knowledge unit

        Raises:
            NotFoundError: If knowledge unit not found
        """
        # Check if exists
        existing = await self.get(id)
        if existing is None:
            raise NotFoundError("KnowledgeUnit", id)

        # Build update clause
        update_fields = []
        params = {"id": id}

        for key, value in data.items():
            if key == "id":
                continue  # Don't update ID
            param_key = f"p_{key}"
            update_fields.append(f"{key} = :{param_key}")

            # Handle special cases
            if key == "context" and isinstance(value, dict):
                import json
                params[param_key] = json.dumps(value)
            elif key == "source" and isinstance(value, Source):
                params[param_key] = value.value
            elif key == "verified" and isinstance(value, bool):
                params[param_key] = 1 if value else 0
            elif isinstance(value, datetime):
                params[param_key] = value.isoformat()
            else:
                params[param_key] = value

        # Always update updated_at
        update_fields.append("updated_at = :updated_at")
        params["updated_at"] = datetime.utcnow().isoformat()

        sql = f"""
            UPDATE {self.TABLE_NAME}
            SET {", ".join(update_fields)}
            WHERE id = :id
        """

        await self.db.execute(sql, params)

        # Return updated entity
        return await self.get(id)

    async def delete(self, id: str) -> bool:
        """Delete knowledge unit.

        Args:
            id: Knowledge unit ID

        Returns:
            True if deleted, False if not found
        """
        sql = f"DELETE FROM {self.TABLE_NAME} WHERE id = :id"
        await self.db.execute(sql, {"id": id})

        # Check if deleted
        return await self.get(id) is None

    async def search(
        self,
        query: str,
        tags: list[str] | None = None,
        limit: int = 10,
        min_confidence: float | None = None,
        source: Source | None = None,
        verified_only: bool = False
    ) -> list[SearchResult]:
        """Full-text search with FTS5.

        Args:
            query: Search query (FTS5 syntax)
            tags: Optional tag filters
            limit: Maximum results
            min_confidence: Minimum confidence level
            source: Filter by source
            verified_only: Only return verified knowledge

        Returns:
            List of search results with rank
        """
        # Build base query - FTS5 with external content mode
        sql = f"""
            SELECT ku.*, bm25({self.FTS_TABLE}) as rank
            FROM {self.TABLE_NAME} ku
            JOIN {self.FTS_TABLE} ON ku.rowid = {self.FTS_TABLE}.rowid
            WHERE {self.FTS_TABLE} MATCH :query
        """

        params: dict[str, Any] = {"query": query}

        # Add filters
        if min_confidence is not None:
            sql += " AND ku.confidence >= :min_confidence"
            params["min_confidence"] = min_confidence

        if source:
            sql += " AND ku.source = :source"
            params["source"] = source.value

        if verified_only:
            sql += " AND ku.verified = 1"

        if tags:
            for i, tag in enumerate(tags):
                sql += f" AND json_extract(ku.context, '$.tags') LIKE :tag{i}"
                params[f"tag{i}"] = f'%{tag}%'

        # Order and limit
        sql += f" ORDER BY ku.confidence DESC, rank LIMIT {limit}"

        rows = await self.db.fetchall(sql, params)

        results = []
        for row in rows:
            rank = row.pop("rank")
            knowledge = KnowledgeUnit.from_db_dict(row)
            results.append(SearchResult(knowledge=knowledge, rank=rank))

        return results

    async def list(
        self,
        filters: ListFilter | None = None,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "created_at",
        order_desc: bool = True
    ) -> list[KnowledgeUnit]:
        """List knowledge units with filters.

        Args:
            filters: Filter criteria
            limit: Maximum results
            offset: Number of results to skip
            order_by: Field to order by
            order_desc: True for descending, False for ascending

        Returns:
            List of knowledge units
        """
        sql = f"SELECT * FROM {self.TABLE_NAME}"
        params: dict[str, Any] = {}

        conditions = []

        if filters:
            if filters.tags:
                for i, tag in enumerate(filters.tags):
                    conditions.append(
                        f"json_extract(context, '$.tags') LIKE :tag{i}"
                    )
                    params[f"tag{i}"] = f'%{tag}%'

            if filters.source:
                conditions.append("source = :source")
                params["source"] = filters.source.value

            if filters.verified is not None:
                conditions.append("verified = :verified")
                params["verified"] = 1 if filters.verified else 0

            if filters.min_confidence is not None:
                conditions.append("confidence >= :min_confidence")
                params["min_confidence"] = filters.min_confidence

            if filters.max_confidence is not None:
                conditions.append("confidence <= :max_confidence")
                params["max_confidence"] = filters.max_confidence

            if filters.created_after:
                conditions.append("created_at >= :created_after")
                params["created_after"] = filters.created_after.isoformat()

            if filters.created_before:
                conditions.append("created_at <= :created_before")
                params["created_before"] = filters.created_before.isoformat()

            if filters.updated_after:
                conditions.append("updated_at >= :updated_after")
                params["updated_after"] = filters.updated_after.isoformat()

            if filters.updated_before:
                conditions.append("updated_at <= :updated_before")
                params["updated_before"] = filters.updated_before.isoformat()

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        # Order by
        direction = "DESC" if order_desc else "ASC"
        sql += f" ORDER BY {order_by} {direction}"

        # Limit and offset
        sql += f" LIMIT {limit} OFFSET {offset}"

        rows = await self.db.fetchall(sql, params)
        return [KnowledgeUnit.from_db_dict(row) for row in rows]

    async def count(self, filters: ListFilter | None = None) -> int:
        """Count knowledge units with filters.

        Args:
            filters: Filter criteria

        Returns:
            Number of matching knowledge units
        """
        sql = f"SELECT COUNT(*) as count FROM {self.TABLE_NAME}"
        params: dict[str, Any] = {}

        conditions = []

        if filters:
            if filters.tags:
                for i, tag in enumerate(filters.tags):
                    conditions.append(
                        f"json_extract(context, '$.tags') LIKE :tag{i}"
                    )
                    params[f"tag{i}"] = f'%{tag}%'

            if filters.source:
                conditions.append("source = :source")
                params["source"] = filters.source.value

            if filters.verified is not None:
                conditions.append("verified = :verified")
                params["verified"] = 1 if filters.verified else 0

            if filters.min_confidence is not None:
                conditions.append("confidence >= :min_confidence")
                params["min_confidence"] = filters.min_confidence

            if filters.max_confidence is not None:
                conditions.append("confidence <= :max_confidence")
                params["max_confidence"] = filters.max_confidence

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        result = await self.db.fetchone(sql, params)
        return result["count"] if result else 0

    async def increment_usage(self, id: str) -> KnowledgeUnit | None:
        """Increment usage count for a knowledge unit.

        Args:
            id: Knowledge unit ID

        Returns:
            Updated knowledge unit, or None if not found
        """
        sql = f"""
            UPDATE {self.TABLE_NAME}
            SET usage_count = usage_count + 1
            WHERE id = :id
        """
        await self.db.execute(sql, {"id": id})
        return await self.get(id)

    async def get_by_tag(self, tag: str, limit: int = 100) -> builtins.list[KnowledgeUnit]:
        """Get knowledge units by tag.

        Args:
            tag: Tag to search for
            limit: Maximum results

        Returns:
            List of knowledge units with the tag
        """
        sql = f"""
            SELECT * FROM {self.TABLE_NAME}
            WHERE json_extract(context, '$.tags') LIKE :tag
            ORDER BY confidence DESC
            LIMIT :limit
        """
        rows = await self.db.fetchall(sql, {"tag": f"%{tag}%", "limit": limit})
        return [KnowledgeUnit.from_db_dict(row) for row in rows]

    async def get_low_confidence(
        self,
        threshold: float = 0.3,
        limit: int = 10
    ) -> builtins.list[KnowledgeUnit]:
        """Get low confidence knowledge units that need review.

        Args:
            threshold: Confidence threshold (below this)
            limit: Maximum results

        Returns:
            List of low confidence knowledge units
        """
        sql = f"""
            SELECT * FROM {self.TABLE_NAME}
            WHERE confidence < :threshold
            ORDER BY usage_count DESC
            LIMIT :limit
        """
        rows = await self.db.fetchall(sql, {
            "threshold": threshold,
            "limit": limit
        })
        return [KnowledgeUnit.from_db_dict(row) for row in rows]

    async def get_recent(self, limit: int = 10) -> builtins.list[KnowledgeUnit]:
        """Get recently updated knowledge units.

        Args:
            limit: Maximum results

        Returns:
            List of recent knowledge units
        """
        sql = f"""
            SELECT * FROM {self.TABLE_NAME}
            ORDER BY updated_at DESC
            LIMIT :limit
        """
        rows = await self.db.fetchall(sql, {"limit": limit})
        return [KnowledgeUnit.from_db_dict(row) for row in rows]

    async def get_tags(self, limit: int = 50) -> builtins.list[tuple[str, int]]:
        """Get tag statistics.

        Args:
            limit: Maximum results

        Returns:
            List of (tag, count) tuples
        """
        sql = f"""
            SELECT value as tag, COUNT(*) as count
            FROM {self.TABLE_NAME}, json_each(json_extract(context, '$.tags'))
            GROUP BY value
            ORDER BY count DESC
            LIMIT :limit
        """
        rows = await self.db.fetchall(sql, {"limit": limit})
        return [(row["tag"], row["count"]) for row in rows]
