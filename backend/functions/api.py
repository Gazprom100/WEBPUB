from netlify.functions import NetlifyFunction
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# Импортируем все роуты
from app.api import auth, channels, posts, metrics, settings

# Подключаем роуты
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(channels.router, prefix="/channels", tags=["channels"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(settings.router, prefix="/settings", tags=["settings"])

# Создаем функцию Netlify
handler = Mangum(app)

# Экспортируем функцию
netlify_function = NetlifyFunction(handler) 