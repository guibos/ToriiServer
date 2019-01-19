from src.domain.value_object import UserNewValueObject

test_user_okabe_rintarou = UserNewValueObject(
    username='OkabeRintarou%20',
    password='I am mad scientist.',
    enabled=True,
    admin=False,
    parental_control=False,
    birth_date=None,
)