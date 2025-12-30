from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings

from src.apps.esi import router as esi_v1

# Disable docs in production
if settings.IS_PRODUCTION:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI(
        title="Esi Service API",
        version="1.0.0",
        description="Backend API for Esi Service",
    )

# Include versioned routers
app.include_router(esi_v1.router, prefix="/api/v1")

# CORS settings
allowed_origins = settings.ALLOWED_ORIGINS.split(",") if settings.ALLOWED_ORIGINS else []
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allows all origins or specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI with PostgreSQL, JWT, and API Versioning!"}
