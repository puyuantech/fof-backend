import traceback

from flask import current_app

from models import User, ManagerInfo, ManagerUserMap
from bases.constants import StuffEnum
from bases.globals import db


def create_manager_and_admin(admin_username, admin_password, manager_id, name, id_type, id_number, address, legal_person):
    u = User.create(
        username=admin_username,
        password=admin_password,
        role_id=StuffEnum.ADMIN,
        is_staff=True,
    )
    try:
        m = ManagerInfo(
            manager_id=manager_id,
            name=name,
            id_type=id_type,
            id_number=id_number,
            address=address,
            legal_person=legal_person,
        )
        m_map = ManagerUserMap(
            user_id=u.id,
            manager_id=manager_id,
        )
        db.session.add(m)
        db.session.add(m_map)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        u.delete()
        current_app.logger.error(traceback.format_exc())
        return False
    return True
