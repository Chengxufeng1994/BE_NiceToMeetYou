from datetime import datetime

from pydantic import BaseModel


class News(BaseModel):
    id: int
    title: str
    link: str
    content: str
    published_at: datetime
