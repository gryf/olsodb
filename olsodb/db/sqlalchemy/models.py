from oslo_db.sqlalchemy import models
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class _Base(models.ModelBase):
    pass


DeclarativeBase = declarative_base(cls=_Base)


class Product(DeclarativeBase):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False, index=True)
    price = Column(Integer)

    company_id = Column(Integer, ForeignKey('companies.id'), index=True)
    company = relationship("Company", back_populates="products")

    def update(self, data):
        for attr in ('name', 'price'):
            try:
                setattr(self, attr, data[attr])
            except KeyError:
                pass


class Company(DeclarativeBase):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False, index=True)

    products = relationship("Product", back_populates="company")

    def update(self, data):
        attr = 'name'
        try:
            setattr(self, attr, data[attr])
        except KeyError:
            pass
