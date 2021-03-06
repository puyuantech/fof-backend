"""manager secret

Revision ID: 3c4c965beace
Revises: 0edaf08f0556
Create Date: 2021-03-17 11:54:38.496838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c4c965beace'
down_revision = '0edaf08f0556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manager_secret',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('manager_id', sa.String(length=32), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('secret', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('manager_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('manager_secret')
    # ### end Alembic commands ###
