import asyncio
from typing import AsyncGenerator, Callable, Generator
from fastapi import FastAPI

from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
import pytest
import pytest_asyncio
from app.db.models import Base
from app.tests.functional.test_db import engine, async_session
import httpx

settings.access_token_algo = 'HS256'
settings.access_token_pubkey = 'topsecret'

@pytest.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture()
async def db_session():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.close()

@pytest.fixture()
def override_get_session(db_session: AsyncSession) -> Callable:
    async def _override():
        yield db_session
    return _override

@pytest.fixture()
def app(override_get_session: Callable) -> FastAPI:
    from app.main import app
    from app.dependencies import get_db_session

    app.dependency_overrides[get_db_session] = override_get_session
    return app

@pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with httpx.AsyncClient(app=app, base_url='http://test') as client:
        yield client
