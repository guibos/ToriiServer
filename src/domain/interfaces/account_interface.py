"""Account Interface."""

from abc import ABCMeta, abstractmethod
from typing import Dict, List, Set, Iterable

from src.domain.entities.user_entity import UserEntity


class AccountInterface(metaclass=ABCMeta):
    """Account Domain Repository Interface."""
    @abstractmethod
    def add_users(self, *, user_entities: Iterable[UserEntity]) -> None:
        """Get session entity from session id."""

    @abstractmethod
    def get_users(self, *, filters: Dict, entity_fields: Set[str]) -> List[UserEntity]:
        pass

    @abstractmethod
    def delete_users(self, *, filters: Dict) -> None:
        pass
