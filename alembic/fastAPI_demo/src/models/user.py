from sqlalchemy import Column, String, Date
from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    address = Column(String)
