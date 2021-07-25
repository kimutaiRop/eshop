import graphene

import auth.schema
import products.schema


class Query(products.schema.Query, auth.schema.Query, graphene.ObjectType):
    pass


class Mutation(auth.schema.Mutation, products.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
