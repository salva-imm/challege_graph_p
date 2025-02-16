import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager


load_dotenv()


DATABASE_URL = os.environ.get("DATABASE_URL")

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@asynccontextmanager
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session