"""info statistics

Revision ID: 9c3a1821c37e
Revises: d81241fc2c84
Create Date: 2021-04-09 15:09:32.309070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c3a1821c37e'
down_revision = 'd81241fc2c84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('info_statistics',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('info_id', sa.Integer(), nullable=True),
    sa.Column('info_type', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.Column('investor_id', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('info_statistics')
    # ### end Alembic commands ###