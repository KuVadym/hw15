from datetime import datetime

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


Base = declarative_base()

class NewsList(Base):
    __tablename__ = "news_list"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=False)
    link = Column(String(100), nullable=False, unique=False)
    news = relationship("News", cascade="all, delete", backref="newslist")

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    subtitle = Column(String(150), nullable=False, unique=False)
    text = Column(String(1000), nullable=False, unique=False)
    news_id = Column(Integer, ForeignKey(NewsList.id, ondelete="CASCADE"))
