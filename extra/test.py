from inspect import getfullargspec
from typing import Iterable

from src.domain.entities.user_entity import UserEntity
from src.common import Permission


class CheckPermissions:
    def __init__(self, *, required_permissions: Iterable):
        self._required_permission = required_permissions

    def __call__(self, func):
        def wrapper(*, current_user, **kwargs):
            if 'current_user' in getfullargspec(func).kwonlyargs:
                return func(current_user=current_user, **kwargs)
            return func(**kwargs)

        return wrapper






@check_permissions(required_permissions={Permission.USER_ADD})
def summing(): pass


summing(current_user=UserEntity(admin=True))

