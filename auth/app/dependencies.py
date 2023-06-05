from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_session
from app.persistance.permission_dao import PermissionDao
from app.service.authorization_service import AuthorizationService
from app.service.token_service import TokenService
from app.db.database import async_session

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session

def get_permission_dao(
        session: AsyncSession = Depends(get_db_session)
    ) -> PermissionDao:
    return PermissionDao(session)

def get_token_service() -> TokenService:
    return TokenService()

def get_authorization_service(
    perm_dao: PermissionDao = Depends(get_permission_dao),
    token_service: TokenService = Depends(get_token_service)
    ) -> AuthorizationService:
    return AuthorizationService(perm_dao, token_service)
