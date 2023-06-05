from typing import List
from app.persistance.permission_dao import PermissionDao
from app.schemas.auth_schemas import GrantedPermission, Permission
from app.service.token_service import TokenService

class AuthorizationService:

    def __init__(self, dao: PermissionDao, token_service: TokenService) -> None:
        self._dao = dao
        self._token_service = token_service

    async def grant_permission(self, request: GrantedPermission) -> None:
        await self._dao.grant_user_permission(request) 

    async def revoke_permission(self, request: GrantedPermission) -> None:
        await self._dao.revoke_user_permission(request)

    async def get_permissions_by_user_id(self, user_id: int) -> List[Permission]:
        return await self._dao.get_permissions_by_user_id(user_id)
