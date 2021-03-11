"""init

Revision ID: 158b3b76aed7
Revises: 
Create Date: 2021-03-11 13:22:25.985655

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '158b3b76aed7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('captcha_img',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.CHAR(length=64), nullable=True),
    sa.Column('value', sa.CHAR(length=64), nullable=True),
    sa.Column('expires_at', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('custom_index',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=31), nullable=True),
    sa.Column('desc', sa.String(length=255), nullable=True),
    sa.Column('recent_1m_ret', mysql.DOUBLE(), nullable=True),
    sa.Column('recent_3m_ret', mysql.DOUBLE(), nullable=True),
    sa.Column('recent_6m_ret', mysql.DOUBLE(), nullable=True),
    sa.Column('recent_y1_ret', mysql.DOUBLE(), nullable=True),
    sa.Column('recent_y3_ret', mysql.DOUBLE(), nullable=True),
    sa.Column('recent_y5_ret', mysql.DOUBLE(), nullable=True),
    sa.Column('mdd', mysql.DOUBLE(), nullable=True),
    sa.Column('sharpe', mysql.DOUBLE(), nullable=True),
    sa.Column('last_unit_nav', mysql.DOUBLE(), nullable=True),
    sa.Column('annualized_ret', mysql.DOUBLE(), nullable=True),
    sa.Column('annualized_vol', mysql.DOUBLE(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('custom_index_nav',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('index_id', sa.Integer(), nullable=True),
    sa.Column('datetime', sa.Date(), nullable=True),
    sa.Column('nav', mysql.DOUBLE(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hedge_allocation',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('fof_id', mysql.CHAR(length=16), nullable=True),
    sa.Column('fund_id', mysql.CHAR(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hedge_comments',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('fund_id', mysql.CHAR(length=16), nullable=True),
    sa.Column('comment', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('info_detail',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=63), nullable=True),
    sa.Column('info_type', sa.Integer(), nullable=True),
    sa.Column('content_type', sa.Integer(), nullable=True),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.Column('is_effected', sa.BOOLEAN(), nullable=True),
    sa.Column('effect_time', sa.DATETIME(), nullable=True),
    sa.Column('effect_user_name', sa.String(length=63), nullable=True),
    sa.Column('create_user_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('info_templates',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('info_to_production',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('info_id', sa.Integer(), nullable=True),
    sa.Column('fof_id', sa.CHAR(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('investor_tags',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tag_name', sa.String(length=16), nullable=True),
    sa.Column('investor_id', sa.String(length=32), nullable=True),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.Column('add_user_id', sa.Integer(), nullable=True),
    sa.Column('del_user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('manager_user_map',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mobile_code',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mobile', sa.CHAR(length=11), nullable=True),
    sa.Column('value', sa.CHAR(length=64), nullable=True),
    sa.Column('action', sa.CHAR(length=31), nullable=True),
    sa.Column('try_times', sa.Integer(), nullable=True),
    sa.Column('success_times', sa.Integer(), nullable=True),
    sa.Column('expires_at', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('operations',
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
    op.create_table('super_admin',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.Column('last_login', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tag_name', sa.String(length=16), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_investor_info',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('investor_id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('nationality', sa.String(length=32), nullable=True),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('mobile_phone', sa.String(length=20), nullable=True),
    sa.Column('landline_phone', sa.String(length=20), nullable=True),
    sa.Column('profession', sa.String(length=32), nullable=True),
    sa.Column('job', sa.String(length=32), nullable=True),
    sa.Column('postcode', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('investor_id'),
    sa.UniqueConstraint('mobile_phone')
    )
    op.create_table('user_manager_info',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('manager_id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=127), nullable=True),
    sa.Column('id_type', sa.Integer(), nullable=True),
    sa.Column('id_number', sa.String(length=127), nullable=True),
    sa.PrimaryKeyConstraint('manager_id')
    )
    op.create_table('users',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mobile', sa.String(length=20), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_staff', sa.BOOLEAN(), nullable=True),
    sa.Column('staff_name', sa.String(length=20), nullable=True),
    sa.Column('is_wx', sa.BOOLEAN(), nullable=True),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.Column('last_login', sa.DATETIME(), nullable=True),
    sa.Column('last_login_investor', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mobile')
    )
    op.create_table('wechat_token',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.CHAR(length=255), nullable=True),
    sa.Column('expires_at', sa.DATETIME(), nullable=False),
    sa.Column('token_type', sa.CHAR(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hedge_favorites',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('fund_id', mysql.CHAR(length=16), nullable=True),
    sa.Column('user_id', mysql.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('super_token',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=32), nullable=True),
    sa.Column('refresh_key', sa.String(length=32), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['super_admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tokens',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=32), nullable=True),
    sa.Column('refresh_key', sa.String(length=32), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.String(length=32), nullable=True),
    sa.Column('investor_id', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_investor_map',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('investor_id', sa.String(length=32), nullable=False),
    sa.Column('map_type', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_unit_map',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manager_id', sa.String(length=32), nullable=False),
    sa.Column('investor_id', sa.String(length=32), nullable=False),
    sa.Column('investor_type', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('cred_type', sa.String(length=20), nullable=True),
    sa.Column('cred', sa.String(length=64), nullable=True),
    sa.Column('mobile', sa.String(length=20), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('sign_date', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=True),
    sa.Column('origin', sa.String(length=20), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('sponsor', sa.String(length=20), nullable=True),
    sa.Column('salesman', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['investor_id'], ['user_investor_info.investor_id'], ),
    sa.ForeignKeyConstraint(['manager_id'], ['user_manager_info.manager_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_we_chat',
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.Column('update_time', sa.DATETIME(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('union_id', sa.CHAR(length=128), nullable=True),
    sa.Column('open_id', sa.CHAR(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_we_chat')
    op.drop_table('user_unit_map')
    op.drop_table('user_investor_map')
    op.drop_table('tokens')
    op.drop_table('super_token')
    op.drop_table('hedge_favorites')
    op.drop_table('wechat_token')
    op.drop_table('users')
    op.drop_table('user_manager_info')
    op.drop_table('user_investor_info')
    op.drop_table('tags')
    op.drop_table('super_admin')
    op.drop_table('operations')
    op.drop_table('mobile_code')
    op.drop_table('manager_user_map')
    op.drop_table('investor_tags')
    op.drop_table('info_to_production')
    op.drop_table('info_templates')
    op.drop_table('info_detail')
    op.drop_table('hedge_comments')
    op.drop_table('hedge_allocation')
    op.drop_table('custom_index_nav')
    op.drop_table('custom_index')
    op.drop_table('captcha_img')
    # ### end Alembic commands ###
