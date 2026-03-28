# Feedback Repository

"""Repository for feedback history."""

import logging
from typing import Any

from cq.core.models import Feedback
from cq.core.storage import Database
from cq.core.scoring import calculate_confidence
from cq.repositories.base import BaseRepository, NotFoundError
from cq.repositories.knowledge import KnowledgeRepository

logger = logging.getLogger(__name__)


class FeedbackRepository(BaseRepository[Feedback]):
    """Repository for feedback on knowledge units."""

    TABLE_NAME = "feedback_history"

    def __init__(self, database: Database, ku_repo: KnowledgeRepository | None = None):
        """Initialize repository.

        Args:
            database: Database instance
            ku_repo: Optional knowledge repository for auto-updating confidence
        """
        super().__init__(database)
        self._ku_repo = ku_repo

    async def create(self, entity: Feedback) -> Feedback:
        """Create a new feedback record.

        Args:
            entity: Feedback to create

        Returns:
            Created feedback
        """
        data = entity.to_db_dict()
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f":{k}" for k in data.keys()])

        sql = f"""
            INSERT INTO {self.TABLE_NAME} ({columns})
            VALUES ({placeholders})
        """

        await self.db.execute(sql, data)
        logger.debug(f"Created feedback: {entity.id} for KU: {entity.ku_id}")

        # Auto-update confidence for the associated knowledge unit
        await self._update_ku_confidence(entity.ku_id)

        return entity

    async def _update_ku_confidence(self, ku_id: str) -> None:
        """Update confidence score for a knowledge unit based on feedback.

        Args:
            ku_id: Knowledge unit ID
        """
        try:
            # Get feedback stats
            stats = await self.get_feedback_stats(ku_id)

            # Calculate new confidence
            new_confidence = calculate_confidence(
                helpful_count=stats["helpful_count"],
                not_helpful_count=stats["not_helpful_count"],
            )

            # Update knowledge unit confidence
            if self._ku_repo:
                ku = await self._ku_repo.get(ku_id)
                if ku:
                    old_confidence = ku.confidence
                    await self._ku_repo.update(ku_id, {"confidence": new_confidence})
                    logger.info(
                        f"Updated confidence for KU {ku_id}: "
                        f"{old_confidence:.3f} -> {new_confidence:.3f} "
                        f"(helpful={stats['helpful_count']}, "
                        f"not_helpful={stats['not_helpful_count']})"
                    )
                else:
                    logger.warning(f"Knowledge unit {ku_id} not found for confidence update")
            else:
                logger.debug("No ku_repo provided, skipping confidence auto-update")
        except Exception as e:
            logger.error(f"Failed to update confidence for KU {ku_id}: {e}")

    async def get(self, id: str) -> Feedback | None:
        """Get feedback by ID.

        Args:
            id: Feedback ID

        Returns:
            Feedback if found, None otherwise
        """
        sql = f"SELECT * FROM {self.TABLE_NAME} WHERE id = :id"
        row = await self.db.fetchone(sql, {"id": id})

        if row is None:
            return None

        return Feedback.from_db_dict(row)

    async def get_by_ku_id(
        self,
        ku_id: str,
        helpful_only: bool | None = None,
        limit: int = 100
    ) -> list[Feedback]:
        """Get feedback for a knowledge unit.

        Args:
            ku_id: Knowledge unit ID
            helpful_only: Filter by helpful status
            limit: Maximum results

        Returns:
            List of feedback records
        """
        sql = f"""
            SELECT * FROM {self.TABLE_NAME}
            WHERE ku_id = :ku_id
        """
        params: dict[str, Any] = {"ku_id": ku_id, "limit": limit}

        if helpful_only is not None:
            sql += " AND helpful = :helpful"
            params["helpful"] = 1 if helpful_only else 0

        sql += " ORDER BY feedback_at DESC LIMIT :limit"

        rows = await self.db.fetchall(sql, params)
        return [Feedback.from_db_dict(row) for row in rows]

    async def update(self, id: str, data: dict[str, Any]) -> Feedback:
        """Update feedback.

        Args:
            id: Feedback ID
            data: Fields to update

        Returns:
            Updated feedback

        Raises:
            NotFoundError: If feedback not found
        """
        # Check if exists
        existing = await self.get(id)
        if existing is None:
            raise NotFoundError("Feedback", id)

        # Build update clause
        update_fields = []
        params = {"id": id}

        for key, value in data.items():
            if key == "id":
                continue
            param_key = f"p_{key}"
            update_fields.append(f"{key} = :{param_key}")

            if key == "helpful" and isinstance(value, bool):
                params[param_key] = 1 if value else 0
            else:
                params[param_key] = value

        sql = f"""
            UPDATE {self.TABLE_NAME}
            SET {", ".join(update_fields)}
            WHERE id = :id
        """

        await self.db.execute(sql, params)

        # Return updated entity
        return await self.get(id)

    async def delete(self, id: str) -> bool:
        """Delete feedback.

        Args:
            id: Feedback ID

        Returns:
            True if deleted, False if not found
        """
        # Get feedback before deletion to update confidence after
        feedback = await self.get(id)
        ku_id = feedback.ku_id if feedback else None

        sql = f"DELETE FROM {self.TABLE_NAME} WHERE id = :id"
        await self.db.execute(sql, {"id": id})

        # Check if deleted
        deleted = await self.get(id) is None

        # Update confidence if feedback was deleted
        if deleted and ku_id:
            await self._update_ku_confidence(ku_id)

        return deleted

    async def list(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[Feedback]:
        """List feedback records with optional filters.

        Args:
            filters: Optional filter criteria (ku_id, helpful, source)
            limit: Maximum results
            offset: Number of results to skip

        Returns:
            List of feedback records
        """
        sql = f"SELECT * FROM {self.TABLE_NAME}"
        params: dict[str, Any] = {}

        conditions = []

        if filters:
            if "ku_id" in filters and filters["ku_id"]:
                conditions.append("ku_id = :ku_id")
                params["ku_id"] = filters["ku_id"]

            if "helpful" in filters and filters["helpful"] is not None:
                conditions.append("helpful = :helpful")
                params["helpful"] = 1 if filters["helpful"] else 0

            if "source" in filters and filters["source"]:
                conditions.append("source = :source")
                params["source"] = filters["source"]

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY feedback_at DESC"
        sql += f" LIMIT {limit} OFFSET {offset}"

        rows = await self.db.fetchall(sql, params)
        return [Feedback.from_db_dict(row) for row in rows]

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count feedback records with filters.

        Args:
            filters: Optional filter criteria

        Returns:
            Number of feedback records
        """
        sql = f"SELECT COUNT(*) as count FROM {self.TABLE_NAME}"
        params: dict[str, Any] = {}

        conditions = []

        if filters:
            if "ku_id" in filters and filters["ku_id"]:
                conditions.append("ku_id = :ku_id")
                params["ku_id"] = filters["ku_id"]

            if "helpful" in filters and filters["helpful"] is not None:
                conditions.append("helpful = :helpful")
                params["helpful"] = 1 if filters["helpful"] else 0

            if "source" in filters and filters["source"]:
                conditions.append("source = :source")
                params["source"] = filters["source"]

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        result = await self.db.fetchone(sql, params)
        return result["count"] if result else 0

    async def get_feedback_stats(
        self,
        ku_id: str
    ) -> dict[str, int]:
        """Get feedback statistics for a knowledge unit.

        Args:
            ku_id: Knowledge unit ID

        Returns:
            Dict with helpful_count, not_helpful_count, total_count
        """
        sql = f"""
            SELECT
                SUM(CASE WHEN helpful = 1 THEN 1 ELSE 0 END) as helpful,
                SUM(CASE WHEN helpful = 0 THEN 1 ELSE 0 END) as not_helpful,
                COUNT(*) as total
            FROM {self.TABLE_NAME}
            WHERE ku_id = :ku_id
        """

        result = await self.db.fetchone(sql, {"ku_id": ku_id})

        return {
            "helpful_count": result["helpful"] or 0,
            "not_helpful_count": result["not_helpful"] or 0,
            "total_count": result["total"] or 0,
        }

    async def delete_by_ku_id(self, ku_id: str) -> int:
        """Delete all feedback for a knowledge unit.

        Args:
            ku_id: Knowledge unit ID

        Returns:
            Number of deleted records
        """
        # Get count before delete
        count_result = await self.db.fetchone(
            f"SELECT COUNT(*) as count FROM {self.TABLE_NAME} WHERE ku_id = :ku_id",
            {"ku_id": ku_id}
        )
        count = count_result["count"] if count_result else 0

        # Delete
        await self.db.execute(
            f"DELETE FROM {self.TABLE_NAME} WHERE ku_id = :ku_id",
            {"ku_id": ku_id}
        )

        return count
