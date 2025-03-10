from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from app.database.db_connection import get_db_session
from app.entities.news import News as NewsEntity
from app.models.news import News
from app.models.pagination import Pagination
from app.repositories.news_mapper import news_entity_to_model


class NewsRepository:
    def __init__(self, db: AsyncSession = Depends(get_db_session)):
        self.db = db

    async def get_news_list(
        self,
        page: int = 1,
        limit: int = 10,
    ) -> tuple[list[News], Pagination]:
        stmt = (
            select(NewsEntity)
            .limit(limit)
            .offset((page - 1) * limit)
            .order_by(NewsEntity.id.desc())
        )
        async with self.db as session:
            total_count = (
                await session.execute(
                    select(func.count()).select_from(NewsEntity),
                )
            ).scalar()
            if total_count is None:
                return [], Pagination(
                    page=page,
                    limit=limit,
                    total_count=0,
                    total_pages=0,
                )
            total_pages = (total_count + limit - 1) // limit
            result = await session.execute(stmt)
            news_entities = result.scalars().all()
            return [news_entity_to_model(news_entity) for news_entity in news_entities], Pagination(
                page=page,
                limit=limit,
                total_count=total_count,
                total_pages=total_pages,
            )

    async def get_news_by_id(self, news_id: int) -> News:
        stmt = select(NewsEntity).where(NewsEntity.id == news_id)
        async with self.db as session:
            result = await session.execute(stmt)
            news_entity = result.scalars().first()
            if news_entity is None:
                raise Exception('News not found')
            return news_entity_to_model(news_entity)
