"""admin setting

Revision ID: 86219ad45e07
Revises: da6216481fdd
Create Date: 2021-03-25 13:59:49.007874

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '86219ad45e07'
down_revision = 'da6216481fdd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('manager_email_account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_ssl', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('port', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('secret', sa.String(length=63), nullable=True))
        batch_op.add_column(sa.Column('sender', sa.String(length=127), nullable=True))
        batch_op.add_column(sa.Column('server', sa.String(length=127), nullable=True))
        batch_op.add_column(sa.Column('username', sa.String(length=63), nullable=True))
        batch_op.drop_column('app_id')
        batch_op.drop_column('app_sec')
        batch_op.drop_column('token')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('manager_email_account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', mysql.VARCHAR(length=127), nullable=True))
        batch_op.add_column(sa.Column('app_sec', mysql.VARCHAR(length=127), nullable=True))
        batch_op.add_column(sa.Column('app_id', mysql.VARCHAR(length=127), nullable=True))
        batch_op.drop_column('username')
        batch_op.drop_column('server')
        batch_op.drop_column('sender')
        batch_op.drop_column('secret')
        batch_op.drop_column('port')
        batch_op.drop_column('is_ssl')

    # ### end Alembic commands ###