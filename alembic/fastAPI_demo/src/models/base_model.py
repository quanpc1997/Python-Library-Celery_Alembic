from sqlalchemy import Column, String, DateTime, UUID, Boolean
from datetime import datetime
from .db import Base
import uuid


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4())
    created_by = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)
