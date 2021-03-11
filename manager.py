from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps import create_app
from models import *

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db, render_as_batch=True)
manager.add_command('db', MigrateCommand)


@manager.option('--username', dest='username', help='admin username', default='fof_username')
@manager.option('--password', dest='password', help='admin password', default='fof_password')
def init_admin(username, password):

    # create admin
    user_info = User(
        nick_name=username,
        role_id=1,
    )
    user_info = user_info.save()

    user_login = UserLogin(
        user_id=user_info.id,
    )
    user_login.username = username
    user_login.password = password
    user_login.save()
    print('\033[32m {} 创建成功！！！请牢记您的账号和密码。'.format(username))


@manager.option('--username', dest='username', help='admin username', default='fof_username')
@manager.option('--password', dest='password', help='admin password', default='fof_password')
def init_super_admin(username, password):

    _admin = SuperAdmin(
        username=username,
        password=password,
    )
    db.session.add(_admin)
    db.session.commit()
    print('\033[32m {} 创建成功！！！请牢记您的账号和密码。'.format(username))


@manager.option('--id', dest='fof_id', help='fof id', default=None)
def update_fof(fof_id):
    from scripts.refresh_fof import update_fof
    update_fof(fof_id)


if __name__ == '__main__':
    manager.run()


