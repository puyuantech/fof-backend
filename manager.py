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
@manager.option('--manager_id', dest='manager_id', help='manager_id', default=None)
def update_fof(fof_id, manager_id):
    from scripts.refresh_fof import update_fof
    update_fof(fof_id, manager_id=manager_id)


@manager.option('--id', dest='fof_id', help='fof id', default=None)
@manager.option('--manager_id', dest='manager_id', help='manager_id', default=None)
def pub_fof(fof_id, manager_id):
    from scripts.refresh_fof import update_public_fof
    update_public_fof(fof_id, manager_id=manager_id)


@manager.option('-l', dest='manager_list', help='to update manager list', action='store_true', default=False)
@manager.option('-m', dest='manager_info', help='to update manager info', action='store_true', default=False)
@manager.option('-f', dest='fund_info', help='to update fund info', action='store_true', default=False)
@manager.option('-s', '--start', dest='start', help='start index', type=int, default=0)
def update_management(manager_list, manager_info, fund_info, start):
    if not any((manager_list, manager_info, fund_info)):
        manager_list = manager_info = fund_info = True
    from scripts.refresh_managements import update_managements
    update_managements(manager_list, manager_info, fund_info, start)


@manager.option('--username', dest='username', help='proxy username')
@manager.option('--password', dest='password', help='proxy password')
def crawl_management(username, password):
    from scripts.crawl_managements import ManagementCrawler
    crawler = ManagementCrawler()
    crawler.setup_proxy(username, password)
    crawler.parallel_craw_funds()


@manager.command
def extend_fof_info():
    from scripts.extend_fof_info import extend_fof_info_from_management
    extend_fof_info_from_management()


if __name__ == '__main__':
    manager.run()


