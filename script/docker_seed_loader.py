
from core.helpers.session_helper import SessionHelper as SHelp
import sqlalchemy


def load_run_sql(filepath):
    '''
    Runs a SQL file using the SQLAlchecmy Session Helper
    '''
    helper = SHelp()
    session = helper.session
    file = open(filepath)
    escaped_sql = sqlalchemy.text(file.read())
    session.execute(escaped_sql)
    session.close()


load_run_sql("../seeds/2019.02.13__14.02.sql")
load_run_sql("../seeds/2019.04.15__14.19.sql")
load_run_sql("../seeds/2019.07.08__09.41.sql")