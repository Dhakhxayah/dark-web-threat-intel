from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.logger import get_logger
from app.routers import alerts, topics, anomalies, graph

logger = get_logger(__name__)
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting " + settings.app_name + " v" + settings.app_version)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.app_version}


app.include_router(alerts.router,    prefix="/api/v1/alerts",    tags=["alerts"])
app.include_router(topics.router,    prefix="/api/v1/topics",    tags=["topics"])
app.include_router(anomalies.router, prefix="/api/v1/anomalies", tags=["anomalies"])
app.include_router(graph.router,     prefix="/api/v1/graph",     tags=["graph"])