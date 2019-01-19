"""Hash service"""

import hashlib
from hmac import compare_digest

from src.common.hash.value_object import HashValueObject

_DEFAULT_HASH_FUNCTION = 'blake2b'
_DEFAULT_HASH_PARAMETERS = {}
_DEFAULT_HASH_STORED_PARAMETERS = {'hash_name': _DEFAULT_HASH_FUNCTION, **_DEFAULT_HASH_PARAMETERS}


def get_default_hash(*, string: str) -> HashValueObject:
    """From a string return a dictionary with hash.

    This function receive a string and generate one HashValueObject:.
    """
    hex_digest = _get_hex_digest_hash_str_function(
        str_hash_function=_DEFAULT_HASH_FUNCTION,
        hash_parameters=_DEFAULT_HASH_PARAMETERS,
        string=string,
    )
    return HashValueObject(hex_digest=hex_digest, **_DEFAULT_HASH_STORED_PARAMETERS)


def verify_data_with_hash(*, string: str, hash_data: HashValueObject) -> bool:
    """From a string and hash library, check if hash is from string."""
    data = hash_data.__dict__
    parameters = {key: data[key] for key in data if key not in ['hash_name', 'hex_digest'] and data[key] is not None}
    hex_digest = _get_hex_digest_hash_str_function(
        str_hash_function=hash_data.hash_name,
        hash_parameters=parameters,
        string=string,
    )
    return compare_digest(hash_data.hex_digest, hex_digest)


def _get_hex_digest_hash_str_function(*, str_hash_function: str, hash_parameters: dict, string: str) -> str:
    """From hash function and hash parameters generate hash of string."""
    hash_function = getattr(hashlib, str_hash_function)(**hash_parameters)
    hash_function.update(string.encode('utf8'))
    return hash_function.hexdigest()
