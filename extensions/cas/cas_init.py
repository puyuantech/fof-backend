from extensions.cas.cas_models.example import CasExample
from cassandra.cqlengine.management import sync_table, drop_table, create_keyspace_simple, create_keyspace_network_topology


def sync_cas_table():
    sync_table(CasExample)


def drop_cas_table():
    drop_table(CasExample)


if __name__ == '__main__':
    from apps import create_app

    from bases.globals import cas
    create_app().app_context().push()
    cas.get_conn()
    cas.get_session()
    sync_cas_table()

    # CasExample.create(
    #     user_id=1,
    #     time_stamp='1',
    # )
    # a = CasExample.get(user_id=1)
    # print(a.to_dict())
    # create_keyspace_simple('fof', 1)
    # create_keyspace_network_topology('fof', {'cn_northwest_1a': 1})
    # drop_cas_table()
