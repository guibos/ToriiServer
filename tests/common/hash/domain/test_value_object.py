"""Test all hash value objects."""
from src.common.hash.value_object import HashValueObject


def test_hash_value_object():
    assert HashValueObject(hex_digest='a', hash_name='b', hash_salt=0)
