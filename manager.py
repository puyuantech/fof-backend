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
    u = User(
        role_id=1,
    )
    u.username = username
    u.password = password
    u.save()
    print('\033[32m {} 创建成功！！！请牢记您的账号和密码。'.format(username))


@manager.option('--id', dest='fof_id', help='fof id', default=None)
def update_fof(fof_id):
    from scripts.refresh_fof import update_fof
    update_fof(fof_id)


@manager.option('--id', dest='fof_id', help='fof id', default=None)
def pub_fof(fof_id):
    from scripts.refresh_fof import update_public_fof
    update_public_fof(fof_id)


if __name__ == '__main__':
    manager.run()


