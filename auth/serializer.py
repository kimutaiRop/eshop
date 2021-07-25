import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import User


class UserType(SQLAlchemyObjectType):
    pk = graphene.Int(source="id")

    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)
