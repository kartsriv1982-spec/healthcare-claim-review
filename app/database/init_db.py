from app.database.db import engine

from app.database.models import Base

# Import models so SQLAlchemy registers them
from app.database.models import Claim
from app.database.audit_models import ClaimAuditLog

Base.metadata.create_all(bind=engine)