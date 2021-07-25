from flask_login import UserMixin
from sqlalchemy import *
from config.database import Base


class User(Base,UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100))
    created = Column(DateTime)
    last_login = Column(DateTime)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_admin = Column(Boolean())
    verified = Column(Boolean())

    def __str__(self):
        return f"{self.username}"
