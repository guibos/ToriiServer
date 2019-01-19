"""Library Interface"""

from abc import ABCMeta, abstractmethod
from typing import Any, Dict


class LibraryInterface(metaclass=ABCMeta):
    """Account Domain Repository."""
    @abstractmethod
    def get_groups_data(self, *, filters: Dict) -> Any:
        # TODO: return a string or a list of entities
        """Get user entity from username."""
