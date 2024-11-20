# Sport 

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    isCoach = Column(Boolean)

class TrainingVideo(Base):
    __tablename__ = 'training_videos'
    id = Column(Integer, primary_key=True)
    duration = Column(Integer)
    resolution = Column(Integer)

class Sport(Base):
    __tablename__ = 'sport'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    rules = Column(String)
    isTeamSport = Column(Boolean, default=True)
