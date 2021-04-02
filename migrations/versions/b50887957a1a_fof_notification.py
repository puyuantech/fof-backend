"""fof notification

Revision ID: b50887957a1a
Revises: 74766296cff9
Create Date: 2021-04-01 16:30:03.910776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b50887957a1a'
down_revision = '74766296cff9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fof_notification',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.Column('investor_id', sa.String(length=32), nullable=True),
    sa.Column('notification_type', sa.String(length=16), nullable=True),
    sa.Column('content', sa.JSON(), nullable=True),
    sa.Column('read', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fof_notification')
    # ### end Alembic commands ###