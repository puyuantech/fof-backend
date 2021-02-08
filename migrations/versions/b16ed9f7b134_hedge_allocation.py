"""hedge allocation

Revision ID: b16ed9f7b134
Revises: 1012842e927b
Create Date: 2021-02-05 10:19:15.933925

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b16ed9f7b134'
down_revision = '1012842e927b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hedge_allocation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fof_id', mysql.CHAR(length=16), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hedge_allocation', schema=None) as batch_op:
        batch_op.drop_column('fof_id')

    # ### end Alembic commands ###