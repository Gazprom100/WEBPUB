from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, channels, posts, metrics, settings
from .core.mongodb import init_mongodb

app = FastAPI(title="WEBPUB API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(channels.router, prefix="/channels", tags=["channels"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(settings.router, prefix="/settings", tags=["settings"])

@app.on_event("startup")
async def startup_event():
    await init_mongodb()

@app.get("/")
async def root():
    return {"message": "Welcome to WEBPUB API"} 