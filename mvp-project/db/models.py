from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tg_id = Column(Integer)
    email = Column(String)


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
