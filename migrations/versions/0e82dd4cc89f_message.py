"""message

Revision ID: 0e82dd4cc89f
Revises: ba9dd5afd7b1
Create Date: 2021-03-22 16:19:58.910284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e82dd4cc89f'
down_revision = 'ba9dd5afd7b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message_task',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=127), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message_task_sub',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=127), nullable=True),
    sa.Column('task_type', sa.Integer(), nullable=False),
    sa.Column('task_content', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['message_task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message_task_sub')
    op.drop_table('message_task')
    # ### end Alembic commands ###
