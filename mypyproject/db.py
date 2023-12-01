# coding: utf-8

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqldb://root@localhost:3306/hotel')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    userid = Column(Integer,primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    role = Column(String(255))

    def get_userid(self):
        return self.userid

    def __repr__(self):
        return "<User(username='%s', password='%s', role='%s')>" % (self.username, self.password, self.role)