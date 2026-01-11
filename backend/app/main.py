"""FastAPI application entry point - POC Version (No Auth Required)."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.background_tasks import background_manager
from app.api.v1 import projects, funnels, track, analytics, events, events


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    # Startup: Initialize default Pinterest project
    from app.services.project_service import ProjectService
    from app.api.v1.projects import DEFAULT_PROJECT_ID
    
    project_service = ProjectService()
    try:
        # Check if default project exists, if not create it
        existing_project = await project_service.get_project_by_id(DEFAULT_PROJECT_ID)
        if not existing_project:
            print(f"Creating default Pinterest project...")
            project = await project_service.create_project(
                org_id="poc-org",
                name="Pinterest",
                domain="Home Feed",  # Pinterest DS: Product Surface / Environment
                project_id=DEFAULT_PROJECT_ID
            )
            print(f"✅ Created default project: {project['name']} (ID: {project['id']})")
            print(f"   API Key: {project['api_key'][:20]}...")
        else:
            print(f"✅ Default project already exists: {existing_project.get('name', 'POC Project')}")
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize default project: {e}")
    
    # Start background tasks
    background_manager.start()
    yield
    # Shutdown: Cleanup (if needed)


app = FastAPI(
    title="IAFA API - POC",
    description="Inspiration-to-Action Funnel Analyzer API (POC - Local Only)",
    version="0.1.0-poc",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Middleware (allow localhost and all origins for POC)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # POC: Allow all origins for local development
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers (no auth required for POC)
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(funnels.router, prefix="/api/v1/funnels", tags=["funnels"])
app.include_router(track.router, prefix="/api/v1/track", tags=["tracking"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "IAFA API - POC (Local Only)",
        "version": "0.1.0-poc",
        "docs": "/docs",
        "note": "This is a POC for data science demonstration. No authentication required."
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "iafa-api-poc"}
