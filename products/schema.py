import os
import graphene
from flask_graphql_auth import mutation_header_jwt_required, get_jwt_identity
from graphene_sqlalchemy import SQLAlchemyConnectionField
from sqlalchemy.exc import IntegrityError
from graphene_file_upload.scalars import Upload
from werkzeug.utils import secure_filename

from config.database import db_session
from products.models import Product
from products.serializer import ProductType
from config.helpers import file_path

class Query(graphene.ObjectType):
    products = SQLAlchemyConnectionField(ProductType.connection)
    product = graphene.Field(ProductType, pk=graphene.Int())

    @classmethod
    def resolve_products(cls, _, info, *args, **kwargs):
        return Product.query.all()

    @classmethod
    def resolve_product(cls, _,info, pk):
        return Product.query.filter_by(id=pk).first()


class ProudctAttribute:
    name = graphene.String()
    description = graphene.String()
    category_id = graphene.Int()
    quantity = graphene.Int()
    price = graphene.Float()
    image = Upload()


class CreateProductInput(graphene.InputObjectType, ProudctAttribute):
    pass


class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        input_ = CreateProductInput(required=True)

    @classmethod
    @mutation_header_jwt_required
    def mutate(cls, _, info, input_):
        input_['owner_id'] = get_jwt_identity()
        file = input_['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(file_path,filename))
        input_['path'] = filename
        input_.pop("image")
        try:
            product = Product(**input_)
            db_session.add(product)
            db_session.commit()
            return CreateProduct(product=product, success=True)
        except IntegrityError as e:
            return CreateProduct(error=f'{e.orig}', success=False)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()