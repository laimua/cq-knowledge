# Storage Module

"""SQLite database connection and management."""

import asyncio
import logging
from pathlib import Path

import aiosqlite

logger = logging.getLogger(__name__)


# Default database path
DEFAULT_DB_PATH = Path.home() / ".cq" / "knowledge.db"


class Database:
    """SQLite database connection manager.

    Provides async connection management with connection pooling
    and automatic schema migration.
    """

    def __init__(self, db_path: Path | None = None):
        """Initialize database manager.

        Args:
            db_path: Path to database file. Defaults to ~/.cq/knowledge.db
        """
        self._db_path = db_path or DEFAULT_DB_PATH
        self._lock = asyncio.Lock()
        self._connection: aiosqlite.Connection | None = None
        self._initialized = False

    @property
    def db_path(self) -> Path:
        """Get database path."""
        return self._db_path

    async def initialize(self) -> None:
        """Initialize database connection and run migrations."""
        if self._initialized:
            return

        async with self._lock:
            if self._initialized:
                return

            # Ensure parent directory exists
            self._db_path.parent.mkdir(parents=True, exist_ok=True)

            # Create connection
            self._connection = await aiosqlite.connect(self._db_path)

            # Mark as initialized before running migrations (needed for internal queries)
            self._initialized = True

            # Enable foreign keys
            await self._connection.execute("PRAGMA foreign_keys = ON")

            # Configure for better performance
            await self._connection.execute("PRAGMA journal_mode = WAL")
            await self._connection.execute("PRAGMA synchronous = NORMAL")

            # Run migrations
            await self._run_migrations()

            logger.info(f"Database initialized: {self._db_path}")

    async def close(self) -> None:
        """Close database connection."""
        async with self._lock:
            if self._connection:
                await self._connection.close()
                self._connection = None
                self._initialized = False
                logger.info("Database connection closed")

    async def execute(
        self,
        sql: str,
        parameters: tuple = (),
        *,
        script: bool = False
    ) -> aiosqlite.Cursor:
        """Execute SQL statement.

        Args:
            sql: SQL statement
            parameters: Query parameters
            script: Whether to execute a script (multiple statements)

        Returns:
            Cursor

        Raises:
            RuntimeError: If database not initialized
        """
        if not self._initialized or not self._connection:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        if script:
            await self._connection.executescript(sql)
        else:
            await self._connection.execute(sql, parameters)

        await self._connection.commit()
        return await self._connection.cursor()

    async def executemany(
        self,
        sql: str,
        parameters: list[tuple]
    ) -> aiosqlite.Cursor:
        """Execute SQL statement with multiple parameter sets.

        Args:
            sql: SQL statement
            parameters: List of parameter tuples

        Returns:
            Cursor

        Raises:
            RuntimeError: If database not initialized
        """
        if not self._initialized or not self._connection:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        await self._connection.executemany(sql, parameters)
        await self._connection.commit()
        return self._connection.cursor()

    async def fetchone(
        self,
        sql: str,
        parameters: tuple = ()
    ) -> dict | None:
        """Fetch one row.

        Args:
            sql: SQL query
            parameters: Query parameters

        Returns:
            Row as dict, or None if not found
        """
        if not self._initialized or not self._connection:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        self._connection.row_factory = aiosqlite.Row
        cursor = await self._connection.execute(sql, parameters)
        row = await cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    async def fetchall(
        self,
        sql: str,
        parameters: tuple = ()
    ) -> list[dict]:
        """Fetch all rows.

        Args:
            sql: SQL query
            parameters: Query parameters

        Returns:
            List of rows as dicts
        """
        if not self._initialized or not self._connection:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        self._connection.row_factory = aiosqlite.Row
        cursor = await self._connection.execute(sql, parameters)
        rows = await cursor.fetchall()

        return [dict(row) for row in rows]

    async def get_version(self) -> int:
        """Get current schema version.

        Returns:
            Schema version number
        """
        try:
            result = await self.fetchone(
                "SELECT MAX(version) as version FROM schema_version"
            )
            return result["version"] if result and result["version"] is not None else 0
        except aiosqlite.DatabaseError:
            # Table doesn't exist yet (first run)
            return 0

    async def _run_migrations(self) -> None:
        """Run pending migrations."""
        current_version = await self.get_version()

        # Get migration files
        migrations_dir = Path(__file__).parent.parent.parent / "migrations"
        if not migrations_dir.exists():
            logger.warning("Migrations directory not found")
            return

        migration_files = sorted(migrations_dir.glob("*.sql"))
        pending_migrations = [
            f for f in migration_files
            if int(f.stem.split("_")[0]) > current_version
        ]

        for migration_file in pending_migrations:
            version = int(migration_file.stem.split("_")[0])
            await self._apply_migration(migration_file, version)

    async def _apply_migration(self, migration_file: Path, version: int) -> None:
        """Apply a single migration.

        Args:
            migration_file: Path to migration file
            version: Migration version number
        """
        logger.info(f"Applying migration: {migration_file.name}")

        sql = migration_file.read_text(encoding="utf-8")
        await self.execute(sql, script=True)

        # Record migration
        await self.execute(
            "INSERT INTO schema_version (version) VALUES (?)",
            (version,)
        )

        logger.info(f"Migration {version} applied successfully")

    async def transaction(self):
        """Get a transaction context manager.

        Usage:
            async with db.transaction():
                # ... operations
        """
        if not self._initialized or not self._connection:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        return self._connection

    async def begin_transaction(self) -> None:
        """Begin a transaction."""
        if not self._initialized or not self._connection:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        await self._connection.execute("BEGIN")

    async def commit(self) -> None:
        """Commit current transaction."""
        if not self._initialized or not self._connection:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        await self._connection.commit()

    async def rollback(self) -> None:
        """Rollback current transaction."""
        if not self._initialized or not self._connection:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        await self._connection.rollback()


# Global database instance
_db_instance: Database | None = None


async def get_database(db_path: Path | None = None) -> Database:
    """Get or create global database instance.

    Args:
        db_path: Optional custom database path

    Returns:
        Database instance
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = Database(db_path)
        await _db_instance.initialize()

    return _db_instance


async def close_database() -> None:
    """Close global database instance."""
    global _db_instance

    if _db_instance:
        await _db_instance.close()
        _db_instance = None
