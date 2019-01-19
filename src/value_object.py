from dataclasses import dataclass

from src.domain.services.account_service import AccountService
from src.infractuture.account_repo import AccountRepository


@dataclass
class AppConfigValueObject:
    cookie_secret: str
    debug: bool
    port: int
    xsrf_cookies: bool
    max_body_size: int
    cache_directory: str


@dataclass
class UserValueObject:
    repository: AccountRepository
    service: AccountService


@dataclass
class CoreValueObject:
    user: UserValueObject
