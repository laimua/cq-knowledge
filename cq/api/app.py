# FastAPI Application

"""FastAPI application factory for Cq Web API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cq.api.routes import api_router
from cq.core.storage import get_database


async def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="Cq Knowledge API",
        description="Stack Overflow for AI Coding Agents - Web API",
        version="0.1.0",
    )

    # Configure CORS for local development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",  # Vite default
            "http://localhost:3000",  # Alternative port
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router, prefix="/api")

    # Startup event - initialize database
    @app.on_event("startup")
    async def startup_event() -> None:
        """Initialize database on application startup."""
        await get_database()

    # Shutdown event - close database connection
    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        """Close database on application shutdown."""
        from cq.core.storage import close_database
        await close_database()

    return app
