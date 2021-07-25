from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from auth.models import User
from config.database import Base


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(200))

    def __str__(self):
        return f"{self.name}"


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)
    description = Column(String(1000))
    price = Column(Float())
    quantity = Column(Integer())
    path = Column(String(200))
    owner_id = Column(Integer, ForeignKey(User.id), nullable=False)
    owner = relationship(User, backref=backref('products', lazy=True))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    category = relationship(Category, backref=backref('products', lazy=True))

    def __str__(self):
        return f'{self.name} - {self.price}'
