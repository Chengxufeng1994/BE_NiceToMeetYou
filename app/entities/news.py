from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime, Integer, String

from app.entities.base import Base


class News(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String, unique=True, index=True)
    content: Mapped[str] = mapped_column(String)
    published_at: Mapped[datetime] = mapped_column(DateTime)
