import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.database.db_connection import get_engine
from app.entities.base import Base
from app.entities.news import News  # noqa: F401
from app.routers.news_router import router as news_router
from app.routers.web_router import router as web_router

logger.remove()
logger.add(sys.stdout, format='{time} {level} {message}', level='INFO')
logger.add('app.log', rotation='10 MB', level='DEBUG')


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()


app = FastAPI(
    title='OneAI Backend Engineer Recruitment Mini-Project',
    version='0.1.0',
    lifespan=lifespan,
)

app.mount('/static', StaticFiles(directory='static'), name='static')


app.include_router(web_router)
app.include_router(news_router)
