# from asgi_lifespan import LifespanManager

# import pytest_asyncio
# from httpx import AsyncClient, ASGITransport


# from main import app


# @pytest_asyncio.fixture(scope="session")
# async def client():
#     async with LifespanManager(app):
#         async with AsyncClient(
#             transport=ASGITransport(app=app),
#             base_url="http://test"
#         ) as ac:
#             yield ac


# import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from main import app
from models import Base
from main import get_session
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
TestSessionLocal = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_test_session():
    async with TestSessionLocal() as session:
        yield session

# Override FastAPI dependency
app.dependency_overrides[get_session] = get_test_session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as ac:
            yield ac
