from fastapi import APIRouter

router = APIRouter(prefix='/health')

@router.get('')
async def health_check():
    return {
        'status': 'OK',
        'message': 'Displaying the health of the service!'
    }
# add more parameters to return here
