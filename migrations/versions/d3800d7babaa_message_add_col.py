"""message add col

Revision ID: d3800d7babaa
Revises: ea0bea7615e1
Create Date: 2021-03-24 15:16:54.587981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3800d7babaa'
down_revision = 'ea0bea7615e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manager_email_account',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.Column('app_id', sa.String(length=127), nullable=True),
    sa.Column('app_sec', sa.String(length=127), nullable=True),
    sa.Column('token', sa.String(length=127), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('manager_id')
    )
    with op.batch_alter_table('message_task_sub', schema=None) as batch_op:
        batch_op.add_column(sa.Column('task_to', sa.TEXT(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message_task_sub', schema=None) as batch_op:
        batch_op.drop_column('task_to')

    op.drop_table('manager_email_account')
    # ### end Alembic commands ###
