from typing import List
from fastapi import APIRouter, Depends, status
from app.dependencies import get_authorization_service

from app.schemas.auth_schemas import GrantedPermission, Permission
from app.service.authorization_service import AuthorizationService

router = APIRouter(prefix='/permission')

@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def grant_user_permission(
    body: GrantedPermission,
    service: AuthorizationService = Depends(get_authorization_service)
    ) -> None:
    await service.grant_permission(body)

@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def revoke_user_permission(
        body: GrantedPermission,
        service: AuthorizationService = Depends(get_authorization_service)
    ) -> None:
    await service.revoke_permission(body)

@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def get_user_permissions(
        user_id: int,
        service: AuthorizationService = Depends(get_authorization_service)
    ) -> List[Permission]:
    return await service.get_permissions_by_user_id(user_id)
