import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
# import os
# from dotenv import load_dotenv

# Only Production
# load_dotenv(dotenv_path = '.env')

# db_user = os.getenv("db_user")
# db_pass = os.getenv("db_pass")
# db_host = os.getenv("db_host")
# db_port = os.getenv("db_port")
# db_name = os.getenv("db_name")

# db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
# ssl_args = {'sslmode':'require'}
# engine = _sql.create_engine(db_string,connect_args=ssl_args, echo=True)

# Only Dev
DATABASE_URL    = ""
engine          = _sql.create_engine(DATABASE_URL)
SessionLocal    = _orm.sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base            = _declarative.declarative_base()