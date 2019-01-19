from src.common.environment import Environment
from src.infractuture.configuration.configuration_repository import Configuration

TEST_DEFAULT_CONFIG_DATA = {
    'database': {
        'username': 'test_default_database_username',
        'password': 'test_default_database_password',
    },
    'toriiserver': {
        'password': 'test_default_toriiserver_password',
        'token': 'test_default_toriiserver_token',
    },
}

PRODUCTION_DEFAULT_CONFIG_DATA = {
    'database': {
        'username': 'production_default_database_username',
        'password': 'production_default_database_password',
    },
    'toriiserver': {
        'password': 'production_default_toriiserver_password',
        'token': 'production_default_toriiserver_token',
    },
}

PRODUCTION_USER_CONFIG_DATA = {
    'database': {
        'username': 'production_default_database_username',
        'password': 'production_user_database_password',
    },
    'toriiserver': {
        'password': 'production_default_toriiserver_password',
        'token': 'production_default_toriiserver_token',
    },
}

YAML_DEFAULT_CONFIG_DATA = \
    "general:\n" \
    "  environment: test\n" \
    "database:\n" \
    "  test:\n" \
    "    username: test_default_database_username\n" \
    "    password: test_default_database_password\n" \
    "  production:\n" \
    "    username: production_default_database_username\n" \
    "    password: production_default_database_password\n" \
    "toriiserver:\n" \
    "  test:\n" \
    "    password: test_default_toriiserver_password\n" \
    "    token: test_default_toriiserver_token\n" \
    "  production:\n" \
    "    password: production_default_toriiserver_password\n" \
    "    token: production_default_toriiserver_token\n"

YAML_USER_CONFIG_DATA_FORCE = \
    "general:\n" \
    "  environment: production\n" \
    "database:\n" \
    "  production:\n" \
    "    password: production_user_database_password\n"

PATH_DEFAULT = "configuration-default.yaml"

USER_DEFAULT = "configuration.yaml"


def test_only_default_configuration(tmpdir):
    default_config_path = tmpdir.join(PATH_DEFAULT)
    user_config_path = tmpdir.join(USER_DEFAULT)

    with open(default_config_path, 'w') as configfile:
        configfile.write(YAML_DEFAULT_CONFIG_DATA)
    config_reader = Configuration(default_config_path=default_config_path, user_config_path=user_config_path)
    assert TEST_DEFAULT_CONFIG_DATA['toriiserver'] == config_reader.get_section(section='toriiserver')
    assert TEST_DEFAULT_CONFIG_DATA['database'] == config_reader.get_section(section='database')


def test_only_default_configuration_force(tmpdir):
    default_config_path = tmpdir.join(PATH_DEFAULT)
    user_config_path = tmpdir.join(USER_DEFAULT)

    with open(default_config_path, 'w') as configfile:
        configfile.write(YAML_DEFAULT_CONFIG_DATA)
    config_reader = Configuration(default_config_path=default_config_path, user_config_path=user_config_path, environment=Environment.PRODUCTION)
    assert PRODUCTION_DEFAULT_CONFIG_DATA['toriiserver'] == config_reader.get_section(section='toriiserver')
    assert PRODUCTION_DEFAULT_CONFIG_DATA['database'] == config_reader.get_section(section='database')


def test_default_and_user_configuration(tmpdir):
    default_config_path = tmpdir.join(PATH_DEFAULT)

    with open(default_config_path, 'w') as configfile:
        configfile.write(YAML_DEFAULT_CONFIG_DATA)

    user_config_path = tmpdir.join(USER_DEFAULT)

    with open(user_config_path, 'w') as configfile:
        configfile.write(YAML_USER_CONFIG_DATA_FORCE)

    config_reader = Configuration(default_config_path=default_config_path, user_config_path=user_config_path)
    assert PRODUCTION_USER_CONFIG_DATA['toriiserver'] == config_reader.get_section(section='toriiserver')
    assert PRODUCTION_USER_CONFIG_DATA['database'] == config_reader.get_section(section='database')
