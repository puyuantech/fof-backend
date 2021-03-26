"""admin setting

Revision ID: d9da63806f26
Revises: 86219ad45e07
Create Date: 2021-03-25 18:17:58.154494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9da63806f26'
down_revision = '86219ad45e07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('manager_wx_account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('encoding_aes_key', sa.String(length=127), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('manager_wx_account', schema=None) as batch_op:
        batch_op.drop_column('encoding_aes_key')

    # ### end Alembic commands ###
