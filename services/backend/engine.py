import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("BACKEND_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres")


engine = create_async_engine(   
    DATABASE_URL
)
main_session = async_sessionmaker(autocommit=False, bind=engine)


async def get_session():
    async with main_session() as session:
        yield session
