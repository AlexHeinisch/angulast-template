from fastapi import FastAPI
from app.endpoint.authorization_endpoint import router as authorization_router
from app.endpoint.health_endpoint import router as health_router

app = FastAPI(
    title='Angular-FastAPI Stack Template'
)

app.include_router(router=authorization_router)
app.include_router(router=health_router)
