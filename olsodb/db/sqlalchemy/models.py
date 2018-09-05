from oslo_db.sqlalchemy import models
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer
from sqlalchemy import String


class _Base(models.ModelBase):
    pass


DeclarativeBase = declarative_base(cls=_Base)


class Foo(DeclarativeBase):
    __tablename__ = 'oslodb'
    id = Column(Integer, primary_key=True)
    value = Column(String(39), nullable=False)
