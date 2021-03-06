"""investor operation

Revision ID: 0b93ccbd55c8
Revises: f0bcf0d15872
Create Date: 2021-04-19 15:02:47.258838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b93ccbd55c8'
down_revision = 'f0bcf0d15872'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('operations_investor',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('investor_id', sa.String(length=32), nullable=True),
    sa.Column('ip', sa.String(length=31), nullable=True),
    sa.Column('action', sa.String(length=31), nullable=True),
    sa.Column('url', sa.TEXT(), nullable=True),
    sa.Column('method', sa.String(length=15), nullable=True),
    sa.Column('request_data', sa.TEXT(), nullable=True),
    sa.Column('response_data', sa.TEXT(), nullable=True),
    sa.Column('response_status', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('operations_investor')
    # ### end Alembic commands ###
