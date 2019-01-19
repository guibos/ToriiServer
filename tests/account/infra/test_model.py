"""Test model of user infrastructure."""
from datetime import date, datetime

from src.infractuture.user_models import UserModel

SING_UP = datetime(year=2018, month=1, day=1, hour=12, minute=30, second=0)
BIRTH_DATE = date(year=2018, month=1, day=1)
USER_DATA = {
    'id': 1,
    'username': "username",
    'password': {},
    'sign_up': SING_UP,
    'enabled': True,
    'admin': True,
    'parental_control': False,
    'birth_date': BIRTH_DATE,
}


def test_user_model():
    """Check if user model is working as expected"""
    UserModel(**USER_DATA)
