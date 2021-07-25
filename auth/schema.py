import graphene
from flask_graphql_auth import create_access_token, create_refresh_token, mutation_jwt_refresh_token_required, \
    get_jwt_identity, query_header_jwt_required
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from auth.models import User
from auth.serializer import UserType
from config.database import db_session
from config.helpers import check


class Register(graphene.Mutation):
    error = graphene.String()
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)

    @classmethod
    def mutate(cls, _, info, email, username, password1, password2):
        if not check(email):
            return Register(error="Make sure you pass correct email")
        if password1 != password2:
            return Register(error="passwords did not match")
        try:
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password1, method="sha256")
            )

            db_session.add(new_user)
            db_session.commit()
        except IntegrityError as e:
            return Register(error=f'{e.orig}')
        return Register(success=True, message="user created")


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        email = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()
    error = graphene.String()

    @classmethod
    def mutate(cls, _, info, email, password):
        if not check(email):
            return AuthMutation(error="invalid email")
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return AuthMutation(error="Bad username or password")
        return AuthMutation(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(cls, _):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(identity=current_user))


class Mutation(graphene.ObjectType):
    register = Register.Field()
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    @classmethod
    @query_header_jwt_required
    def resolve_me(cls, info, *args):
        user_id = get_jwt_identity()
        return User.query.filter_by(id=user_id).first()
