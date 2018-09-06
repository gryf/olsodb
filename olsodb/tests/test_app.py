import unittest

from oslo_db.sqlalchemy import enginefacade

from olsodb.app import main
from olsodb.db.sqlalchemy import models


class TestApp(unittest.TestCase):

    def tearDown(self):
        # Remove all the data from db. In real life, we don't want that.
        eng = enginefacade.writer.get_engine()
        models.DeclarativeBase.metadata.drop_all(eng)

    def test_create_company(self):
        app = main.App()
        company = app.create_company({'name': 'Commodore'})
        self.assertEqual(company.name, 'Commodore')

    def test_get_company(self):
        app = main.App()
        company = app.create_company({'name': 'Commodore'})
        self.assertEqual(company.name, 'Commodore')

        companies = app.get_company()
        self.assertEqual(len(companies), 1)
        self.assertEqual(companies[0].name, 'Commodore')

        company = app.create_company({'name': 'Atari'})
        self.assertEqual(company.name, 'Atari')

        companies = app.get_company()
        self.assertEqual(len(companies), 2)
        self.assertListEqual(sorted([c.name for c in companies]),
                             ['Atari', 'Commodore'])


if __name__ == "__main__":
    unittest.main()
