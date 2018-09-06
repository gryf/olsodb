from olsodb.db import api


class App(object):
    """
    Simple app class, which provide interface for creating, retrieving,
    updating and removing DB object Foo.

    Simplest usage:

        app = olsodb.app.main.App()
        app.create_company(data)

        where data is a simple dictionary with corresponding columns in foo
        table, i.e.

        {'value': some_new_value,
         'id': identifier_of_the_object}

        Note, that in certain situations, 'id' will or will not be used -
        updating will not change object id in the db.
    """

    def __init__(self):
        api.configure({'connection': 'sqlite://'})
        api.create_schema()
        self.ctx = api.get_context()

    def get_company(self, data=None):
        """return list of Foo objects, which match value"""
        return(api.read_companies(self.ctx, data))

    def update_company(self, data):
        """Update Foo object, which match value with new_value"""
        return(api.update_company(self.ctx, data))

    def create_company(self, data):
        """Create Foo object"""
        return(api.create_company(self.ctx, data))

    def delete_company(self, company_id):
        """return list of Foo objects, which match 'value'"""
        return(api.delete_company(self.ctx, company_id))
