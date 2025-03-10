from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    limit: int
    total_count: int
    total_pages: int
