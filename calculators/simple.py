import pandas as pd
from models import MobileCode
from bases.globals import db
from apps import create_app
create_app().app_context().push()

query = db.session.query(MobileCode)
df = pd.read_sql(query.statement, query.session.bind)
print(df)

from surfing.data.wrapper.mysql import BasicDatabaseConnector
from surfing.data.view.basic_models import FOFInfo

with BasicDatabaseConnector().managed_session() as session:
    query = session.query(FOFInfo)
    info = pd.read_sql(query.statement, query.session.bind)
    print(info)





