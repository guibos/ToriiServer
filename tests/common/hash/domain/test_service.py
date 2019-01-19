"""Test of Domain HashService Module."""
import src.common.hash.service as hash_service
from src.common.hash.value_object import HashValueObject

STRING = 'verysecurepassword'

HASH_DATA = HashValueObject(
    hex_digest='2d1f0a18b2e100f1cf78a8a665e39195a9526d068382508eea4296679e1cdb5e85c8af020aa42dc19bacc875080ab8ef18409b2'
    'eb269527ee0723bf49d826dbf',
    hash_name='blake2b',
)

HASH_DATA_WRONG = HashValueObject(
    hex_digest='wrong218b2e100f1cf78a8a665e39195a9526d068382508eea4296679e1cdb5e85c8af020aa42dc19bacc875080ab8ef18409b2'
    'eb269527ee0723bf49d826dbf',
    hash_name='blake2b',
)


def test_get_default_hash():
    """Check a normal execution of HashService.get_default_hash."""
    b = hash_service.get_default_hash(string=STRING)
    assert b == HASH_DATA


def test_get_default_hash_abnormal():
    """Check a abnormal execution of HashService.get_default_hash."""
    b = hash_service.get_default_hash(string=STRING)
    assert b != HASH_DATA_WRONG


def test_verify_data_with_hash():
    """Check a normal execution of HashService.verify_data_with_hash."""
    assert hash_service.verify_data_with_hash(string=STRING, hash_data=HASH_DATA)


def test_verify_data_with_hash_abnormal():
    """Check a normal execution of HashService.verify_data_with_hash."""
    assert not hash_service.verify_data_with_hash(string=STRING, hash_data=HASH_DATA_WRONG)
