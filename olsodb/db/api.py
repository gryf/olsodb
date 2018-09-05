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
def create_foo(context, value):
    return IMPL.create_foo(context, value)


def read_foos(context, value=None):
    return IMPL.read_foos(context, value=None)


def update_foo(context, old_value, new_value):
    return IMPL.update_foo(context, old_value, new_value)


def delete_foo(context, value):
    return IMPL.delete_foo(context, value)
