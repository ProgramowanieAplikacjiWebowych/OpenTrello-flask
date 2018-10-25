from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER = 'sql7262722'
PASSWORD = '1sWYylgbvZ'
DATABASE = 'sql7262722'
HOST = 'sql7.freesqldatabase.com'
PORT = '3306'
SQL_CONNECTION_STRING = 'mysql+pymysql://' + USER + ':' + PASSWORD + '@' + HOST + ':' + PORT + '/' + DATABASE
engine = create_engine(SQL_CONNECTION_STRING)

Session = sessionmaker(bind=engine)
Base = declarative_base()