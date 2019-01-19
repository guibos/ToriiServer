from src.domain.value_object import UserNewValueObject


def get_admin_user() -> UserNewValueObject:
    return UserNewValueObject(
        username='admin',
        password='admin',
        enabled=True,
        admin=True,
        parental_control=False,
        birth_date=None)
