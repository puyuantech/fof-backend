"""production contract

Revision ID: f8e0004cd5bf
Revises: 2334e7cbd706
Create Date: 2021-04-28 13:29:44.655885

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f8e0004cd5bf'
down_revision = '2334e7cbd706'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('production_contract',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('investor_id', sa.String(length=32), nullable=True),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.Column('fof_id', sa.String(length=16), nullable=True),
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('template_type', sa.String(length=16), nullable=True),
    sa.Column('contract_id', sa.Integer(), nullable=True),
    sa.Column('contract_url_key', sa.String(length=128), nullable=True),
    sa.Column('union_key', sa.String(length=128), nullable=True),
    sa.Column('signed', sa.Boolean(), nullable=True),
    sa.Column('sign_time', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('manager_secret')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manager_secret',
    sa.Column('create_time', mysql.DATETIME(), nullable=True),
    sa.Column('update_time', mysql.DATETIME(), nullable=True),
    sa.Column('is_deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.Column('manager_id', mysql.VARCHAR(length=32), nullable=False),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('secret', mysql.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('manager_id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('production_contract')
    # ### end Alembic commands ###