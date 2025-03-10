from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=['web'],
)

templates = Jinja2Templates(directory='templates')


@router.get('/news')
def news_page(request: Request):
    return templates.TemplateResponse('news_list.html', {'request': request})


@router.get('/news/{news_id}')
def news_detail_page(request: Request):
    return templates.TemplateResponse('news_detail.html', {'request': request})
