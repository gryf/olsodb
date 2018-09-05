import sys

import alembic.migration as alembic_migration
from oslo_config import cfg
from oslo_db.sqlalchemy import enginefacade
from oslo_db import options

from olsodb.db.sqlalchemy import models


storage_context_manager = enginefacade.transaction_context()


@enginefacade.transaction_context_provider
class Context(object):
    pass


class DBMigrationException(Exception):
    pass


class RecordNotFoundException(Exception):
    pass


def configure(conf):
    config = {'sqlite_fk': True, 'max_retries': 5}
    config.update(conf)

    options.set_defaults(cfg.CONF, connection=config['connection'])
    storage_context_manager.configure(**config)


def get_backend():
    return sys.modules[__name__]


def get_context():
    return Context()


def create_schema(config=None, engine=None):
    if engine is None:
        engine = enginefacade.writer.get_engine()

    # This check might be ignored, but in certain point of time it *will* turn
    # out that you need migrations :)
    if version(engine=engine) is not None:
        raise DBMigrationException('DB schema is already under version '
                                   'control. Use upgrade() instead.')

    models.DeclarativeBase.metadata.create_all(engine)


def version(config=None, engine=None):
    if engine is None:
        engine = enginefacade.writer.get_engine()

    with engine.connect() as conn:
        context = alembic_migration.MigrationContext.configure(conn)
        return context.get_current_revision()


@enginefacade.writer
def create_foo(context, value):
    foo = models.Foo()
    foo.value = value
    context.session.add(foo)
    return foo


@enginefacade.reader
def read_foos(context, value=None):
    query = context.session.query(models.Foo)
    if value:
        query = query.filter(models.Foo.value == value)

    return query.all()


@enginefacade.writer
def update_foo(context, old_value, new_value):
    foo = (context.session.query(models.Foo)
           .filter(models.Foo.value == old_value)).one_or_none()

    if not foo:
        raise RecordNotFoundException('Cannot find element with value "%s".',
                                      old_value)

    foo.value = new_value
    foo.save(context.session)
    return foo


@enginefacade.writer
def delete_foo(context, value):
    foo = (context.session.query(models.Foo)
           .filter(models.Foo.value == value)).one_or_none()

    if not foo:
        raise RecordNotFoundException('Cannot find element with value "%s".',
                                      value)

    context.session.delete(foo)
