from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.auth import auth_routes
from .api.v1.employees import employee_routes
from .api.v1.activities import activities_routes
from app.db.session import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    Base.metadata.create_all(bind=engine)
    print("Startup...")
    yield
    # Shutdown:
    print("Shutdown...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Business Activity Tracker API",
        description="RESTful API for managing employee records with secure authentication and business activity tracking",
        version="0.0.1",
        lifespan=lifespan
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API routes
    app.include_router(auth_routes.router)
    app.include_router(employee_routes.router)
    app.include_router(activities_routes.router)

    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": "Business Tracker API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
