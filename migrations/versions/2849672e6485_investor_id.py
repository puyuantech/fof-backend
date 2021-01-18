"""investor id

Revision ID: 2849672e6485
Revises: 05018072a757
Create Date: 2021-01-15 19:01:08.049737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2849672e6485'
down_revision = '05018072a757'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('investor_id', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('investor_id')

    # ### end Alembic commands ###
