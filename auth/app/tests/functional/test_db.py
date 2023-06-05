from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import settings

engine = create_async_engine(settings.test_database_url)
async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
