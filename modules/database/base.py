from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from abc import ABCMeta, abstractmethod

USER = 'sql7262722'
PASSWORD = '1sWYylgbvZ'
DATABASE = 'sql7262722'
HOST = 'db4free.net'
PORT = '3306'
SQL_CONNECTION_STRING = 'mysql+pymysql://' + USER + ':' + PASSWORD + '@' + HOST + ':' + PORT + '/' + DATABASE
engine = create_engine(SQL_CONNECTION_STRING)

Session = sessionmaker(bind=engine)


class DeclarativeABCMeta(DeclarativeMeta, ABCMeta):
    pass


class BaseModel(declarative_base(metaclass=DeclarativeABCMeta)):
    __abstract__ = True
    @abstractmethod
    def serialize(self):
        pass
