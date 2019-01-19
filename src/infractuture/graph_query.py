import graphene

from src.infractuture.graph_schema import UserSchema


class Query(graphene.ObjectType):
    users = graphene.List(UserSchema)

    async def resolve_users(self, info):
        query = UserSchema.get_query(info)  # SQLAlchemy query
        return query.all()
