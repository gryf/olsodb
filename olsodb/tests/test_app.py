import unittest

from oslo_db.sqlalchemy import enginefacade
from sqlalchemy.orm import exc

from olsodb.app import main
from olsodb.db.sqlalchemy import models
from olsodb.db.sqlalchemy import api as saapi


class TestApp(unittest.TestCase):

    def tearDown(self):
        # Remove all the data from db. In real life, we don't want that.
        eng = enginefacade.writer.get_engine()
        models.DeclarativeBase.metadata.drop_all(eng)

    def test_create_company(self):
        app = main.App()
        company = app.create_company({'name': 'Commodore'})
        self.assertEqual(company.name, 'Commodore')

    def test_get_company_no_companies(self):
        app = main.App()
        companies = app.get_company()
        self.assertListEqual(companies, [])

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

    def test_update_company_wrong_argument(self):
        app = main.App()
        self.assertRaises(main.WrongDataException, app.update_company, {})

    def test_update_not_existing_company(self):
        app = main.App()
        self.assertRaises(main.RecordNotFoundException, app.update_company,
                          {'id': 1, 'name': 'Commodore'})

    def test_update_not_company(self):
        app = main.App()
        company = app.create_company({'name': 'Atari'})
        updated = app.update_company({'id': company.id, 'name': 'Commodore'})
        self.assertEqual(updated.id, company.id)
        self.assertEqual(updated.name, 'Commodore')

    def test_delete_company_wrong_argument(self):
        app = main.App()
        self.assertRaises(saapi.RecordNotFoundException,
                          app.delete_company, {})

    def test_delete_not_existing_company(self):
        app = main.App()
        self.assertRaises(exc.NoResultFound, app.delete_company, {'id': 1})

    def test_delete_company(self):
        app = main.App()
        app.create_company({'name': 'Commodore'})
        app.create_company({'name': 'Atari'})

        companies = app.get_company({})
        self.assertEqual(len(companies), 2)
        self.assertListEqual(sorted([c.name for c in companies]),
                             ['Atari', 'Commodore'])


if __name__ == "__main__":
    unittest.main()
