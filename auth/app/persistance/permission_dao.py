from typing import List
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import GrantedPermissionEntity
from app.exceptions import ConflictException, NotFoundException, UnexpectedException

from app.schemas.auth_schemas import GrantedPermission, Permission


class PermissionDao():

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_permissions_by_user_id(self, user_id: int) -> List[Permission]:
        result = await self._session.execute(
            select(GrantedPermissionEntity.permission)
            .where(GrantedPermissionEntity.user_id == user_id)
        )
        return [Permission[r.upper()] for r in result.scalars().all()]

    async def grant_user_permission(self, perm: GrantedPermission) -> None:
        try:
            self._session.add(
                GrantedPermissionEntity(user_id=perm.user_id, permission=perm.permission)
            )
            await self._session.commit()
        except IntegrityError as e:
            if 'duplicate' in str(e):
                raise ConflictException(detail={'message': f'Permission for user {perm} already exists! (duplicate permission)'})
            else:
                raise UnexpectedException(detail={'message': str(e)})

    async def revoke_user_permission(self, perm: GrantedPermission) -> None:
        result = await self._session.execute(
            delete(GrantedPermissionEntity)
            .where(GrantedPermissionEntity.user_id == perm.user_id and GrantedPermissionEntity.permission == perm.permission)
        )
        await self._session.commit()
        if result.rowcount == 0:
            raise NotFoundException(detail={'message': f'Permission not found: {perm}'})
