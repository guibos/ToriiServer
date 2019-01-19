"""User Entity."""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from dataclasses_json import dataclass_json

from src.common.hash.value_object import HashValueObject
from src.domain.permission_enum import Permission


@dataclass_json
@dataclass
class UserEntity:
    """User Entity. This will have all library of a user."""
    id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[HashValueObject] = None
    sign_up: Optional[datetime] = None
    enabled: Optional[bool] = None
    session_active: Optional[datetime] = None
    admin: Optional[bool] = None
    parental_control: Optional[bool] = None
    birth_date: Optional[date] = None

    @property
    def permissions(self) -> set:
        if self.admin:
            return set(Permission)
        else:
            return set()
