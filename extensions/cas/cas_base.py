from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy


class FlaskCas(object):
    def __init__(self, app=None, config_prefix="cas", **kwargs):
        self._cos_client = None
        self.provider_kwargs = kwargs
        self.config_prefix = config_prefix
        self.session = None
        self.conn = None
        self.username = None
        self.password = None
        self.hosts = None
        self.default_key_space = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app, **kwargs):
        config = app.config.copy()

        self.username = config['CAS']['username']
        self.password = config['CAS']['password']
        self.hosts = config['CAS']['hosts']
        self.default_key_space = config['CAS']['default_key_space']

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions[self.config_prefix.lower()] = self

    def init_conn(self):
        if not all([self.username, self.password, self.hosts]):
            raise Exception('No CAS config.')

        if not self.session or not self.conn:
            auth_provider = PlainTextAuthProvider(
                username=self.username,
                password=self.password,
            )
            cluster = Cluster(
                self.hosts,
                auth_provider=auth_provider,
                load_balancing_policy=DCAwareRoundRobinPolicy(),
                protocol_version=4,
            )
            self.session = cluster.connect()
            self.conn = connection.register_connection('', session=self.session, default=True)

    def get_conn(self):
        self.init_conn()
        return self.conn

    def get_session(self):
        self.init_conn()
        return self.session

    def __getattr__(self, name):
        return getattr(self._cos_client, name)

    def __getitem__(self, name):
        return self._cos_client[name]

    def __setitem__(self, name, value):
        self._cos_client[name] = value

    def __delitem__(self, name):
        del self._cos_client[name]

    def get_columns(self, model, columns):
        columns_format = '{},' * (len(columns) - 1) + '{}'
        columns_format = columns_format.format(*columns)

        cql = "SELECT {} from {}.{}".format(
            columns_format,
            model.__keyspace__,
            model.__table_name__,
        )
        return self.session.execute(cql)

    def get_columns_by_id(self, model, columns, id_column, id_value):
        columns_format = '{},' * (len(columns) - 1) + '{}'
        columns_format = columns_format.format(*columns)

        cql = "SELECT {} from {}.{} WHERE {}=?".format(
            columns_format,
            model.__keyspace__,
            model.__table_name__,
            id_column,
        )
        cql_lookup = self.session.prepare(cql)
        cql_lookup.consistency_level = ConsistencyLevel.ONE

        ret = self.session.execute(cql_lookup, [id_value])
        ret = [i for i in ret]
        if len(ret) < 1:
            return None

        return ret[0]

    def scan_columns_by_id(self, model, columns, id_column, id_value):
        columns_format = '{},' * (len(columns) - 1) + '{}'
        columns_format = columns_format.format(*columns)

        cql = "SELECT {} from {}.{} WHERE {}=?".format(
            columns_format,
            model.__keyspace__,
            model.__table_name__,
            id_column,
        )
        cql_lookup = self.session.prepare(cql)
        cql_lookup.consistency_level = ConsistencyLevel.ONE

        return [i for i in self.session.execute(cql_lookup, [id_value])]

    def get_columns_by_two_ids(self, model, columns, id_column, id_value, id_column2, id_value2):
        columns_format = '{},' * (len(columns) - 1) + '{}'
        columns_format = columns_format.format(*columns)

        cql = "SELECT {} from {}.{} WHERE {}=? AND {}=?".format(
            columns_format,
            model.__keyspace__,
            model.__table_name__,
            id_column,
            id_column2,
        )
        cql_lookup = self.session.prepare(cql)
        cql_lookup.consistency_level = ConsistencyLevel.ONE

        ret = self.session.execute(cql_lookup, [id_value, id_value2])
        ret = [i for i in ret]
        if len(ret) < 1:
            return None

        return ret[0]

    def truncate_table(self, model):
        cql = "TRUNCATE table {}.{}".format(
            model.__keyspace__,
            model.__table_name__
        )
        return self.session.execute(cql)
