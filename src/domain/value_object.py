"""User Value Objects"""
from dataclasses import dataclass
from datetime import datetime

# FIXME: there are some problem with dataclass_json: https://github.com/lidatong/dataclasses-json/issues/108
from typing import Optional

from dataclasses_json import dataclass_json

from src.domain.entities.user_entity import UserEntity


@dataclass
class UserLoginValueObject:
    """Define how domain layer will receive the library to authenticate through username and password."""
    username: str
    password: str


@dataclass_json
@dataclass
class UserCookieValueObject:
    """Define how application layer will receive the library to set cookie on client."""
    id: int
    session_active: datetime


@dataclass_json
@dataclass
class UserNewValueObject:
    username: str
    password: str
    enabled: bool
    admin: bool
    parental_control: bool
    birth_date: Optional[datetime]

    @classmethod
    def from_user_entity(cls, *, user_entity: UserEntity):
        return cls(**{key: getattr(user_entity, key) for key in cls.__annotations__.keys()})

    def visible_fields(self):
        user = UserNewValueObject(**self.__dict__)
        user.password = None
        return user
