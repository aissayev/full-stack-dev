print("Добро пожаловать в мой MVP проект")

from models import User
from sqlalchemy import TIMESTAMP, create_engine

from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

SYNC_SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://test:test@localhost:5432/postgres"
)

sync_engine = create_engine(
    SYNC_SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True,
)

sync_session = sessionmaker(
    autocommit=False, autoflush=False, bind=sync_engine, future=True
)

def create_user(name, last, isCoach):
  with sync_session() as session:
    instance = User(
      firstName=name,
      lastName=last,
      isCoach=isCoach,
    )
    session.add(instance)
    session.commit()

name = input("Enter name:")
lastName = input("Enter lastName:")
isCoach = input("Enter isCoach:")

if isCoach == 'True':
  create_user(name, lastName, True)
else:
  create_user(name, lastName, False)