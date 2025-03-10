from typing import Annotated, Generic, TypeVar

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.models.news import News
from app.repositories.news_repository import NewsRepository
from app.services.news_service import NewsService

T = TypeVar('T')  # 定義泛型類型


class PaginationResponse(BaseModel, Generic[T]):
    page: int  # 當前頁數
    limit: int  # 當前返回的數量
    total_pages: int  # 總頁數
    total_count: int  # 總數量
    data: list[T]  # 具體的數據


router = APIRouter(
    prefix='/api/news',
    tags=['news'],
)


def get_news_service(
    news_repository: NewsRepository = Depends(),
) -> NewsService:
    return NewsService(news_repository)


async def pagination_params(
    q: str | None = None,
    page: int = 1,
    limit: int = 10,
):
    return {'q': q, 'page': page, 'limit': limit}


@router.get('/', response_model=PaginationResponse)
async def get_news_list(
    paginationParams: Annotated[dict, Depends(pagination_params)],
    news_service: NewsService = Depends(get_news_service),
):
    try:
        result, pagination = await news_service.get_news_list(
            paginationParams['page'], paginationParams['limit']
        )
        return PaginationResponse(
            page=pagination.page,
            limit=pagination.limit,
            total_pages=pagination.total_pages,
            total_count=pagination.total_count,
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/{news_id}', response_model=News)
async def get_news_detail(
    news_id: int,
    news_service: NewsService = Depends(get_news_service),
):
    try:
        news = await news_service.get_news_by_id(news_id)
        return news
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
