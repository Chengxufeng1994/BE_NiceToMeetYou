from fastapi import Depends

from app.models.news import News
from app.models.pagination import Pagination
from app.repositories.news_repository import NewsRepository


class NewsService:
    news_repository: NewsRepository

    def __init__(
        self,
        news_repository: NewsRepository = Depends(),
    ):
        self.news_repository = news_repository

    async def get_news_list(
        self,
        page: int = 1,
        limit: int = 10,
    ) -> tuple[list[News], Pagination]:
        return await self.news_repository.get_news_list(page, limit)

    async def get_news_by_id(self, news_id: int) -> News:
        return await self.news_repository.get_news_by_id(news_id)
