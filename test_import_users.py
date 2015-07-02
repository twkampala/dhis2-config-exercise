from unittest import TestCase
from import_users_csv import UserMetaDataGenerator
from mock import MagicMock

class UserMetaDataGeneratorTestCase(TestCase):
    def test_build_user_list(self):
        generator = UserMetaDataGenerator("file.csv", "url", "username", "password")
        generator.get_data_rows = MagicMock(return_value=["Erin,Prohaska,eprohaska,eprohaska@gmail.com,Project Level User Role,secret"])
        users = generator.build_user_list()
        self.assertEquals(len(users), 1)
        self.assertEquals(users[0]["name"], "Erin Prohaska")
        self.assertEquals(users[0]["displayName"], "Erin Prohaska")
        self.assertEquals(users[0]["id"], "tb70de18777")
        self.assertEquals(users[0]["firstName"], "Erin")
        self.assertEquals(users[0]["surname"], "Prohaska")
        self.assertEquals(users[0]["userCredentials"], {"username": "eprohaska", "password": "secret", "disabled": False, 'userRoles': [{'id': 't189972b334', 'name': 'Project Level User Role'}],})
