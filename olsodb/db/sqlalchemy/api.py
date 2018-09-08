import sys

from oslo_config import cfg
from oslo_db.sqlalchemy import enginefacade
from oslo_db import options

from olsodb.db.sqlalchemy import models


storage_context_manager = enginefacade.transaction_context()


@enginefacade.transaction_context_provider
class Context(object):
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

    models.DeclarativeBase.metadata.create_all(engine)


@enginefacade.writer
def create_company(context, data):
    company = models.Company()
    if 'id' in data:
        del data['id']
    company.update(data)
    context.session.add(company)
    return company


@enginefacade.reader
def read_companies(context, data):
    query = context.session.query(models.Company)
    if 'id' in data:
        query = query.filter(models.Company.id == data['id'])
    if 'name' in data:
        query = query.filter(models.Company.name == data['name'])

    return query.all()


@enginefacade.writer
def update_company(context, data):
    query = context.session.query(models.Company)
    if 'id' in data:
        company = query.filter(models.Company.id == data['id']).one()
    else:
        raise RecordNotFoundException('Cannot update Company without '
                                      'company id')

    company.update(data)
    company.save(context.session)
    return company


@enginefacade.writer
def delete_company(context, data):
    query = context.session.query(models.Company)
    if 'id' in data:
        company = query.filter(models.Company.id == data['id']).one()
    else:
        raise RecordNotFoundException('Cannot delete Company without '
                                      'company id')

    context.session.delete(company)


@enginefacade.writer
def create_product(context, data):
    company = models.Company()
    if 'id' in data:
        del data['id']
    company.update(data)
    context.session.add(company)
    return company


@enginefacade.reader
def read_products(context, id_=None, name=None, price=None):
    query = context.session.query(models.Company)
    if id_:
        query = query.filter(models.Company.id == id_)
    if name:
        query = query.filter(models.Company.name == 'name')

    return query.all()


@enginefacade.writer
def update_product(context, data):
    query = context.session.query(models.Company)
    if 'id' in data:
        company = query.filter(models.Company.id == data['id']).one()
    else:
        raise RecordNotFoundException('Cannot update Company without '
                                      'company id')

    company.update(data)
    company.save(context.session)
    return company


@enginefacade.writer
def delete_product(context, data):
    query = context.session.query(models.Company)
    if 'id' in data:
        company = query.filter(models.Company.id == data['id']).one()
    else:
        raise RecordNotFoundException('Cannot delete Company without '
                                      'company id')

    context.session.delete(company)


@enginefacade.reader
def get_company_products(context, company_id):
    query = (context.session.query(models.Product)
             .join(models.Company)
             .filter(models.Company.id == company_id))

    return query.all()
