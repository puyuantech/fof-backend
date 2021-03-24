"""wx

Revision ID: ea0bea7615e1
Revises: ecec29050d95
Create Date: 2021-03-24 10:15:56.623531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea0bea7615e1'
down_revision = 'ecec29050d95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message_task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fof_id', sa.String(length=63), nullable=True))

    with op.batch_alter_table('user_we_chat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_url', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('manager_id', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('nick_name', sa.String(length=127), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_we_chat', schema=None) as batch_op:
        batch_op.drop_column('nick_name')
        batch_op.drop_column('manager_id')
        batch_op.drop_column('avatar_url')

    with op.batch_alter_table('message_task', schema=None) as batch_op:
        batch_op.drop_column('fof_id')

    # ### end Alembic commands ###