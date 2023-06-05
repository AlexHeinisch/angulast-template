from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistance.permission_dao import PermissionDao
from app.schemas.auth_schemas import GrantedPermission, Permission

pytestmark = pytest.mark.asyncio

async def test_grant_permission_no_conflict_success(async_client: AsyncClient, db_session: AsyncSession):
    dao = PermissionDao(session=db_session)
    payload = {
        'user_id': 3,
        'permission': Permission.USER.value
    }

    response = await async_client.post('/permission', json=payload)

    assert response.status_code == 204

    permissions = await dao.get_permissions_by_user_id(payload['user_id'])
    assert len(permissions) == 1
    assert permissions[0] == Permission.USER.value

async def test_grant_permission_invalid_permission(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        'user_id': 3,
        'permission': 'SomeInvalidPermission'
    }

    response = await async_client.post('/permission', json=payload)

    assert response.status_code == 422
    assert 'value is not a valid enumeration member' in response.text


async def test_grant_permission_user_already_has_permission(
    async_client: AsyncClient, 
    db_session: AsyncSession
    ):
    dao = PermissionDao(session=db_session)
    
    payload = {
        'user_id': 3,
        'permission': 'USER'
    }

    # introduce already existing permission
    await dao.grant_user_permission(GrantedPermission(user_id=payload['user_id'], permission=Permission[payload['permission'].upper()]))

    response = await async_client.post('/permission', json=payload)
    assert response.status_code == 409
    assert 'duplicate' in response.text.lower()

async def test_grant_permission_missing_user_id(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        'permission': 'USER'
    }

    response = await async_client.post('/permission', json=payload)

    assert response.status_code == 422
    assert 'field required' in response.text

async def test_revoke_permission_success(
    async_client: AsyncClient,
    db_session: AsyncSession
    ):
    dao = PermissionDao(session=db_session)

    payload = {
        'user_id': 3,
        'permission': Permission.USER.value
    }

    await dao.grant_user_permission(GrantedPermission(user_id=payload['user_id'], permission=Permission[payload['permission'].upper()]))

    response = await async_client.request(method='DELETE', url='/permission', json=payload)
    assert response.status_code == 204

async def test_revoke_permission_not_found(
    async_client: AsyncClient,
    db_session: AsyncSession
    ):

    payload = {
        'user_id': 3,
        'permission': Permission.USER.value
    }

    response = await async_client.request(method='DELETE', url='/permission', json=payload)
    assert response.status_code == 404

async def test_revoke_permission_invalid_permission(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        'user_id': 3,
        'permission': 'SomeInvalidPermission'
    }

    response = await async_client.request(method='DELETE', url='/permission', json=payload)

    assert response.status_code == 422
    assert 'value is not a valid enumeration member' in response.text

async def test_revoke_permission_missing_user_id(async_client: AsyncClient, db_session: AsyncSession):
    payload = {
        'permission': Permission.USER.value
    }

    response = await async_client.request(method='DELETE', url='/permission', json=payload)

    assert response.status_code == 422
    assert 'field required' in response.text
