import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Product, Category


class CategoryType(SQLAlchemyObjectType):
    pk = graphene.Int(source="id")

    class Meta:
        model = Category
        interfaces = (relay.Node,)


class ProductType(SQLAlchemyObjectType):
    pk = graphene.Int(source="id")

    class Meta:
        model = Product
        interfaces = (relay.Node,)
