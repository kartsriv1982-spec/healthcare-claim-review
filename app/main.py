from fastapi import FastAPI

from app.api import auth
from app.api import claims
from app.api import dashboard
from app.database.db import engine
from app.database.models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Healthcare Claim Review API",
    version="1.0.0"
)

app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    claims.router,
    prefix="/api/v1/claims",
    tags=["Claims"]
)

app.include_router(
    dashboard.router,
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


@app.get("/health")
def health():

    return {
        "status": "UP"
    }