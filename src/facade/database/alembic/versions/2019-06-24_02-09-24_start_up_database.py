"""Start-up database

Revision ID: 83cfc0f4e557
Revises: 
Create Date: 2019-06-24 02:09:24.433826

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '83cfc0f4e557'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'licensor',
        sa.Column('id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('name',
                  sa.JSON(),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'producer',
        sa.Column('id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('name',
                  sa.JSON(),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'serialization',
        sa.Column('id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('name',
                  sa.JSON(),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'studio',
        sa.Column('id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('name',
                  sa.JSON(),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'type',
        sa.Column('id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('name',
                  sa.JSON(),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'user',
        sa.Column('id',
                  sa.Integer(),
                  autoincrement=True,
                  nullable=False),
        sa.Column('username',
                  sa.String(),
                  nullable=False),
        sa.Column('password',
                  sa.JSON(),
                  nullable=False),
        sa.Column('sign_up',
                  sa.DateTime(timezone=True),
                  nullable=False),
        sa.Column('enabled',
                  sa.Boolean(),
                  nullable=False),
        sa.Column('session_active',
                  sa.DateTime(timezone=True),
                  nullable=False),
        sa.Column('admin',
                  sa.Boolean(),
                  nullable=False),
        sa.Column('parental_control',
                  sa.Boolean(),
                  nullable=False),
        sa.Column('birth_date',
                  sa.Date(),
                  nullable=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table(
        'group',
        sa.Column('id',
                  sa.Integer(),
                  autoincrement=True,
                  nullable=False),
        sa.Column('insert_date',
                  sa.Date(),
                  nullable=False),
        sa.Column('name',
                  sa.JSON(),
                  nullable=True),
        sa.Column('release_date',
                  sa.Date(),
                  nullable=True),
        sa.Column('user_id',
                  sa.Integer(),
                  nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['user.id'],
        ),
        sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'subtype',
        sa.Column('id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('name',
                  sa.JSON(),
                  nullable=True),
        sa.Column('type',
                  sa.Integer(),
                  nullable=True),
        sa.Column('mode',
                  sa.Integer(),
                  nullable=True),
        sa.ForeignKeyConstraint(
            ['type'],
            ['type.id'],
        ),
        sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'title',
        sa.Column('id',
                  sa.Integer(),
                  autoincrement=True,
                  nullable=False),
        sa.Column('insert_date',
                  sa.Date(),
                  nullable=False),
        sa.Column('user_id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('data',
                  sa.JSON(),
                  nullable=True),
        sa.Column('name',
                  sa.JSON(),
                  nullable=True),
        sa.Column('subtype',
                  sa.Integer(),
                  nullable=True),
        sa.Column('release_date',
                  sa.Date(),
                  nullable=True),
        sa.Column('premiered',
                  sa.JSON(),
                  nullable=True),
        sa.Column('broadcast',
                  sa.JSON(),
                  nullable=True),
        sa.ForeignKeyConstraint(
            ['subtype'],
            ['subtype.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['user.id'],
        ),
        sa.PrimaryKeyConstraint('id'))
    op.create_table(
        'group_title',
        sa.Column('group_id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('title_id',
                  sa.Integer(),
                  nullable=False),
        sa.ForeignKeyConstraint(
            ['group_id'],
            ['group.id'],
        ),
        sa.ForeignKeyConstraint(
            ['title_id'],
            ['title.id'],
        ),
        sa.PrimaryKeyConstraint('group_id',
                                'title_id'))
    op.create_table(
        'title_licensor',
        sa.Column('title_id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('licensor_id',
                  sa.Integer(),
                  nullable=False),
        sa.ForeignKeyConstraint(
            ['licensor_id'],
            ['licensor.id'],
        ),
        sa.ForeignKeyConstraint(
            ['title_id'],
            ['title.id'],
        ),
        sa.PrimaryKeyConstraint('title_id',
                                'licensor_id'))
    op.create_table(
        'title_producer',
        sa.Column('title_id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('producer_id',
                  sa.Integer(),
                  nullable=False),
        sa.ForeignKeyConstraint(
            ['producer_id'],
            ['producer.id'],
        ),
        sa.ForeignKeyConstraint(
            ['title_id'],
            ['title.id'],
        ),
        sa.PrimaryKeyConstraint('title_id',
                                'producer_id'))
    op.create_table(
        'title_studio',
        sa.Column('title_id',
                  sa.Integer(),
                  nullable=False),
        sa.Column('studio_id',
                  sa.Integer(),
                  nullable=False),
        sa.ForeignKeyConstraint(
            ['studio_id'],
            ['studio.id'],
        ),
        sa.ForeignKeyConstraint(
            ['title_id'],
            ['title.id'],
        ),
        sa.PrimaryKeyConstraint('title_id',
                                'studio_id'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('title_studio')
    op.drop_table('title_producer')
    op.drop_table('title_licensor')
    op.drop_table('group_title')
    op.drop_table('title')
    op.drop_table('subtype')
    op.drop_table('group')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('type')
    op.drop_table('studio')
    op.drop_table('serialization')
    op.drop_table('producer')
    op.drop_table('licensor')
    # ### end Alembic commands ###
