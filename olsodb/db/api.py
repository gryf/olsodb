from oslo_config import cfg
from oslo_db import api as db_api


_BACKEND_MAPPING = {'sqlalchemy': 'olsodb.db.sqlalchemy.api'}


IMPL = db_api.DBAPI.from_config(cfg.CONF, backend_mapping=_BACKEND_MAPPING)


def configure(conf):
    IMPL.configure(conf)


def get_engine():
    return IMPL.get_engine()


def get_context():
    return IMPL.get_context()


def create_schema():
    IMPL.create_schema()


# CRUD operations
def create_company(context, data):
    return IMPL.create_company(context, data)


def read_companies(context, data):
    return IMPL.read_companies(context, data)


def update_company(context, data):
    return IMPL.update_company(context, data)


def delete_company(context, data):
    return IMPL.delete_company(context, data)


def create_product(context, data):
    return IMPL.create_product(context, data)


def read_products(context, data):
    return IMPL.read_products(context, data)


def update_product(context, data):
    return IMPL.update_product(context, data)


def delete_product(context, data):
    return IMPL.delete_product(context, data)


def get_company_products(context, data):
    return IMPL.get_company_products(context, data)
