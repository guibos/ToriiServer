"""Add data

Revision ID: ec482521222d
Revises: 83cfc0f4e557
Create Date: 2019-06-24 02:10:05.745055

"""

from alembic import context

# revision identifiers, used by Alembic.
from src.domain.entities.user_entity import UserEntity
from src.domain.services.account_service import AccountService
from src.infractuture.account_repo import AccountRepository
from src.facade.database.data import get_admin_user
from src.facade.database.facade import DatabaseFacade
from src.facade.database.value_object import DatabaseURLValueObject

revision = 'ec482521222d'
down_revision = '83cfc0f4e557'
branch_labels = None
depends_on = None


def upgrade():
    # TODO: Check more polite way to add admin user.
    user = get_admin_user()
    database_url_config = DatabaseURLValueObject(
        drivername=context.config.get_main_option('database_url.drivername'),
        username=context.config.get_main_option('database_url.username'),
        password=context.config.get_main_option('database_url.password'),
        host=context.config.get_main_option('database_url.host'),
        port=context.config.get_main_option('database_url.port'),
        database=context.config.get_main_option('database_url.database'),
        query=context.config.get_main_option('database_url.query'),
    )
    database_facade = DatabaseFacade(database_url_config=database_url_config)
    account_repository = AccountRepository(database_facade=database_facade)
    account_service = AccountService(account_repository=account_repository)

    account_service.add_users(current_user=UserEntity(**user.__dict__), user_new_value_object_list=[user])


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
