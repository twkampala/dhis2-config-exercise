from unittest import TestCase

from import_users_csv import UserMetaDataGenerator
from mock import MagicMock


class UserMetaDataGeneratorTestCase(TestCase):
    def test_each_user_should_have_the_required_field(self):
        generator = UserMetaDataGenerator("file.csv", "url", "username", "password")
        generator.get_data_rows = MagicMock(
            return_value=["Erin,Prohaska,eprohaska,eprohaska@gmail.com,Project Level User Role,secret"])
        users = generator.build_user_list([], [])
        self.assertEquals(len(users), 1)
        self.assertEquals(users[0]["name"], "Erin Prohaska")
        self.assertEquals(users[0]["displayName"], "Erin Prohaska")
        self.assertEquals(users[0]["id"], "tb70de18777")
        self.assertEquals(users[0]["firstName"], "Erin")
        self.assertEquals(users[0]["surname"], "Prohaska")
        self.assertEquals(users[0]["userCredentials"],
                          {"username": "eprohaska", "password": "secret", "disabled": False,
                           'userRoles': [{'id': 't189972b334', 'name': 'Project Level User Role'}], })

    def test_build_user_list_should_create_structure_for_each_line(self):
        generator = UserMetaDataGenerator("file.csv", "url", "username", "password")
        generator.get_data_rows = MagicMock(
            return_value=["Erin,Prohaska,eprohaska,eprohaska@gmail.com,Project Level User Role,secret",
                          "Deonte,Homenick,dhomenick,dhomenick@yahoo.com,ordinary user,secretPassword"])
        users = generator.build_user_list([], [])
        self.assertEquals(len(users), 2)
        self.assertEquals(users[1]["name"], "Deonte Homenick")

    def test_build_user_list_should_setup_country_level_org_units_for_admin(self):
        country_level_org_units = ["a", "b"]
        generator = UserMetaDataGenerator("file.csv", "url", "username", "password")
        generator.get_data_rows = MagicMock(
            return_value=["Erin,Prohaska,eprohaska,eprohaska@gmail.com,admin user,secret"])
        users = generator.build_user_list(country_level_org_units, [])
        self.assertEquals(len(users), 1)
        self.assertEquals(users[0]["organisationUnits"], country_level_org_units)

    def test_build_user_list_should_setup_project_level_org_units_for_ordinary_user(self):
        project_level_org_units = ["a", "b"]
        generator = UserMetaDataGenerator("file.csv", "url", "username", "password")
        generator.get_data_rows = MagicMock(
            return_value=["Erin,Prohaska,eprohaska,eprohaska@gmail.com,ordinary user,secret"])
        users = generator.build_user_list([], project_level_org_units)
        self.assertEquals(len(users), 1)
        self.assertEquals(users[0]["organisationUnits"], project_level_org_units)
