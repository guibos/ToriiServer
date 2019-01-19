import sqlalchemy as sa

from src.infractuture.user_models import BASE as USER_BASE
from src.facade.database.facade import DatabaseFacade
from src.facade.database.value_object import DatabaseURLValueObject
from src.infractuture.library_models import BASE as LIBRARY_BASE

MULTIPLE_METADATA = [
    LIBRARY_BASE.metadata,
    USER_BASE.metadata,
]


def combine_metadata() -> sa.MetaData:
    m = sa.MetaData()
    for metadata in MULTIPLE_METADATA:
        for t in metadata.tables.values():
            t.tometadata(m)
    return m


def get_production_url(*, database_configuration) -> DatabaseURLValueObject:
    """Get DatabaseURLValueObject with the configuration of configuration file."""
    return DatabaseURLValueObject(**database_configuration)


def get_default_database_facade(*, database_configuration) -> DatabaseFacade:
    """Get DatabaseFacade with the configuration of configuration file."""
    return DatabaseFacade(database_url_config=get_production_url(database_configuration=database_configuration))
