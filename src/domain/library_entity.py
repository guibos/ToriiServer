"""User Value Objects"""
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Title:
    id: int
    name: str


@dataclass_json
@dataclass
class GroupEntity:
    id: int
    name: str
    titles: List[Title]
