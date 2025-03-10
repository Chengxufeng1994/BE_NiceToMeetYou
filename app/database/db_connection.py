from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./database.db'


def get_engine():
    return create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
    )


# sessionmaker for async sessions
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine(),
    class_=AsyncSession,
)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


# === 2️⃣ 設置 SQLAlchemy 連線 ===
BASE_SQLALCHEMY_DATABASE_URL = 'sqlite:///./database.db'
engine = create_engine(BASE_SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
