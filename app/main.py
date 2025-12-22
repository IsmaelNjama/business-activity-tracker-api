from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.auth import auth_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    print("Startup...")
    yield
    # Shutdown:
    print("Shutdown...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="FastAPI Template",
        description="FastAPI Template",
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

    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
