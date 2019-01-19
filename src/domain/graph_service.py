"""User Service"""
import datetime
from typing import Optional, List

import src.common.hash.service as hash_service
from src.domain.entities.user_entity import UserEntity
from src.domain.errors.not_enough_privileges_error import NotEnoughPrivilegesError
from src.domain.interfaces.account_interface import AccountInterface
from src.domain.value_object import UserLoginValueObject, UserCookieValueObject, UserNewValueObject
from src.common import RequestedFilterNotAllowedError
from src.common import FieldMixin
from src.domain.permission_enum import Permission
from src.domain.permission_service import check_permissions


class GraphService(FieldMixin):
    """Account Service."""
    ENTITY = UserEntity

    def __init__(self, *, account_repository: AccountInterface):
        self._account_repository = account_repository
        self._fields = set(UserEntity.__annotations__.keys())
        self._fields_non_visible = {'password', 'session_active'}
        self._fields_visible = {
            field
            for field in UserEntity.__annotations__.keys() if field not in self._fields_non_visible
        }
        self._fields_key = {'id'}

    def auth_user_login(self, *, user_login: UserLoginValueObject) -> Optional[UserCookieValueObject]:
        """Authenticate user through user and password."""
        users = self._account_repository.get_users(
            filters={'username__in': [user_login.username]},
            entity_fields=self._fields)

        if len(users) != 1:
            return None

        user = users[0]

        if not self._is_valid_user(user=user):
            return None

        if not hash_service.verify_data_with_hash(string=user_login.password, hash_data=user.password):
            return None

        cookie_value = UserCookieValueObject(id=user.id, session_active=user.session_active)

        return cookie_value

    def auth_cookie_login(self, *, user_cookie: UserCookieValueObject) -> Optional[UserEntity]:
        """Authenticate user through cookie."""
        users = self._account_repository.get_users(filters={'id__in': [user_cookie.id]}, entity_fields=self._fields)

        if len(users) != 1:
            return None

        user = users[0]

        if not self._is_valid_user(user=user):
            return None

        if user_cookie.session_active != user.session_active:
            return None

        return user

    @check_permissions(required_permissions={Permission.USER_GET})
    def get_users(self, *, arguments: dict):
        users = self._account_repository.get_users(filters=arguments, entity_fields=self._fields_visible)
        return users

    @check_permissions(required_permissions={Permission.USER_ADD})
    def add_users(self, *, current_user: UserEntity, user_new_value_object_list: List[UserNewValueObject]) -> None:
        """Create new user."""
        if not current_user.admin:
            raise NotEnoughPrivilegesError

        users = self._add_users_generate_entities(user_new_value_object_list=user_new_value_object_list)

        self._account_repository.add_users(user_entities=users)

    @staticmethod
    def _add_users_generate_entities(*, user_new_value_object_list: List[UserNewValueObject]):
        for user_new_value_object in user_new_value_object_list:
            # TODO: check data
            data = user_new_value_object.__dict__

            password = hash_service.get_default_hash(string=data.pop('password'))

            yield UserEntity(
                **data,
                password=password,
                sign_up=datetime.datetime.now(),
                session_active=datetime.datetime.now(),
            )

    @check_permissions(required_permissions={Permission.USER_GET, Permission.USER_DEL})
    def delete_users(self, *, current_user: UserEntity, arguments: dict):
        if arguments.keys() - self._fields_key:
            raise RequestedFilterNotAllowedError(arguments.keys() - {current_user.id})

        # TODO: transfer all resources of deleted user to current user

    @staticmethod
    def _is_valid_user(*, user: UserEntity):
        if user is None:
            return False

        if not user.enabled:
            return False

        return True
