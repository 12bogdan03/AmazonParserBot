import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float


from database import Base


class User(Base):
    __tablename__ = "users"

    tg_id = Column(Integer, primary_key=True)
    is_admin = Column(Boolean, default=False)

    def __init__(self, tg_id):
        self.tg_id = tg_id


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    link = Column(String(500))
    title = Column(String(500))
    price = Column(Float)
    added_at = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, link, title=None):
        self.link = link
        self.title = title
