import functools
from inspect import getfullargspec
from typing import Set

from src.domain.entities.user_entity import UserEntity
from src.domain.permission_enum import Permission
from src.domain.permission_error import PermissionDomainError


def check_permissions_function(*, required_permissions: Set[Permission], user: UserEntity):
    if not user:
        raise PermissionDomainError("Non Authenticated User")
    if required_permissions - user.permissions:
        raise PermissionDomainError(f"Not enough permissions: {required_permissions - user.permissions}")
    return True


def check_permissions(*, required_permissions: Set[Permission]):
    def _decorator(func):
        @functools.wraps(func)
        def wrapper(self=None, *, current_user: UserEntity, **kwargs):
            check_permissions_function(required_permissions=required_permissions, user=current_user)
            if 'current_user' in getfullargspec(func).kwonlyargs:
                return func(self, current_user=current_user, **kwargs)
            return func(self, **kwargs)

        return wrapper

    return _decorator
