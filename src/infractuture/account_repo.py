"""User Infrastructure Repository"""
from typing import Dict, Iterable

from src.domain.entities.user_entity import UserEntity
from src.domain.interfaces.account_interface import AccountInterface
from src.infractuture.user_models import UserModel
from src.facade.database.query_mixin import QueryMixin


class AccountRepository(QueryMixin, AccountInterface):
    """Account Infrastructure Repository."""
    _MODEL = UserModel

    def __init__(self, *, database_facade):
        self._database_facade = database_facade

    def add_users(self, *, user_entities: Iterable[UserEntity]):
        with self._database_facade.get_session() as session:
            session.bulk_save_objects(
                [UserModel.from_domain_data(user_entity=user_entity) for user_entity in user_entities])

    def get_users(self, *, filters: Dict, entity_fields: set) -> Iterable[UserEntity]:
        query = self.generate_select_query(filters=filters, entity_fields=entity_fields)
        with self._database_facade.get_connectable() as connection:
            return [self._to_entity(data=dict(user)) for user in connection.execute(query)]

    def delete_users(self, *, filters: Dict) -> None:
        query = self.generate_delete_query(filters=filters)
        with self._database_facade.get_connectable() as connection:
            connection.execute(query)

    def _to_entity(self, *, data: dict) -> UserEntity:
        data = self.fix_datetime_without_timezone(data)
        user_entity = UserEntity.from_dict(data)

        return user_entity
