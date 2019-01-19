"""Hash value Objects"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class HashValueObject:
    """Defines how will be saved hashed library."""
    hex_digest: str
    hash_name: str
    hash_salt: Optional[int] = None
