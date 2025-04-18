from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, channels, posts, metrics, settings
from .core.config import settings as app_settings

app = FastAPI(
    title="CryptoCMS API",
    description="API for managing Telegram channel content",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(channels.router, prefix="/api/channels", tags=["channels"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])

@app.get("/")
async def root():
    return {"message": "Welcome to CryptoCMS API"} 