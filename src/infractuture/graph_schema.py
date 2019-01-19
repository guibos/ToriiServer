import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.infractuture.user_models import UserModel


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        # use `only_fields` to only expose specific fields ie "name"
        # only_fields = ("name",)
        # use `exclude_fields` to exclude specific fields ie "last_name"
        # exclude_fields = ("last_name",)





schema = graphene.Schema(query=Query)
