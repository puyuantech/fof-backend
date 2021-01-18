"""investor position

Revision ID: 05018072a757
Revises: d533ee3ade30
Create Date: 2021-01-15 18:58:53.418928

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '05018072a757'
down_revision = 'd533ee3ade30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fof_scale_alteration', schema=None) as batch_op:
        batch_op.drop_column('unit_total')
        batch_op.drop_column('investor_id')

    with op.batch_alter_table('user_positions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('datetime', sa.DATE(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_positions', schema=None) as batch_op:
        batch_op.drop_column('datetime')

    with op.batch_alter_table('fof_scale_alteration', schema=None) as batch_op:
        batch_op.add_column(sa.Column('investor_id', mysql.CHAR(length=16), nullable=False))
        batch_op.add_column(sa.Column('unit_total', mysql.DOUBLE(asdecimal=True), nullable=True))

    # ### end Alembic commands ###
