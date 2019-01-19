"""Database infrastructure."""
from contextlib import contextmanager

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from src.facade.database.value_object import DatabaseURLValueObject


class DatabaseFacade:
    """Database helper class."""
    def __init__(self, *, database_url_config: DatabaseURLValueObject) -> None:
        """Prepare the Database connection.
        :param database_url_config
        """
        self._engine = sa.create_engine(database_url_config.get_url())

    @contextmanager
    def get_session(self) -> Session:
        Session = sessionmaker(bind=self._engine)
        session = Session()

        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

    @contextmanager
    def get_connectable(self) -> sa.engine.Connection:
        connect: sa.engine.Connection = self._engine.connect()
        try:
            yield connect
        except Exception:
            pass
        finally:
            connect.close()
