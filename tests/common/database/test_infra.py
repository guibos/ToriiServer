from src.facade.database.value_object import DatabaseURLValueObject


def test_database_url_config():
    url = DatabaseURLValueObject(drivername='test').get_url()
    assert url.__str__() == 'test://'
