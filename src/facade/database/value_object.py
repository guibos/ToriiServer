from dataclasses import dataclass

from sqlalchemy.engine.url import URL


@dataclass
class DatabaseURLValueObject:
    """Define all necessary to create a database URL."""
    drivername: str
    username: str = None
    password: str = None
    host: str = None
    port: str = None
    database: str = None
    query: str = None

    def get_url(self):
        return URL(
            drivername=self.drivername,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            query=self.query,
        )
