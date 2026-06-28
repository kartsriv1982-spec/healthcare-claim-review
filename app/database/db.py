from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

# ==================================================
# Database URL
# ==================================================

DATABASE_URL = (

    f"postgresql://"

    f"{settings.DB_USER}:"

    f"{settings.DB_PASSWORD}@"

    f"{settings.DB_HOST}:"

    f"{settings.DB_PORT}/"

    f"{settings.DB_NAME}"

)

# ==================================================
# SQLAlchemy Engine
# ==================================================

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True

)

# ==================================================
# Session Factory
# ==================================================

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)

# ==================================================
# Dependency
# ==================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()