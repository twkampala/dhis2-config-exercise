import hashlib
import json

import requests
from requests.auth import HTTPBasicAuth


class UserMetaDataGenerator(object):
    def __init__(self, csv_path, url, username, password):
        self.csv_path = csv_path
        self.url = url
        self.username = username
        self.password = password

    # id should be 11 characters and start with a letter
    def create_id(self, value):
        return ("t%s" % hashlib.md5(value).hexdigest())[0:11]

    def get_data_rows(self):
        with open(self.csv_path, "r") as file_handle:
            return file_handle.readlines()[1:]

    def build_single_user(self, country_level_org_units, project_org_units):
        def user_func(line):
            first_name, last_name, username, email, role, password = line.strip().split(",")
            name = display_name = "%s %s" % (first_name, last_name)
            role = {"name": role, "id": self.create_id(role)}
            org_units = project_org_units
            if "admin" in role["name"]:
                org_units = country_level_org_units
            return {"firstName": first_name,
                    "name": name,
                    "organisationUnits": org_units,
                    "email": email,
                    "id": self.create_id(name),
                    "displayName": display_name,
                    "surname": last_name,
                    "userCredentials": {"userRoles": [role], "username": username, "password": password,
                                        "disabled": False}}

        return user_func

    def build_user_list(self, country_level_org_units, project_org_units):
        return map(self.build_single_user(country_level_org_units, project_org_units), self.get_data_rows())

    def build_single_role(self, item):
        return {"name": item['name'], "id": self.create_id(item["name"]), "displayName": item['name'],
                "authorities": item["authorities"]}

    def create_roles(self):
        role_definitions = [{"name": "ordinary user",
                             "authorities": ["M_dhis-web-dashboard-integration", "M_dhis-web-maintenance-dataadmin",
                                             "M_dhis-web-visualizer", "M_dhis-web-event-reports",
                                             "M_dhis-web-event-visualizer", "M_dhis-web-pivot", "See My DHIS",
                                             "M_dhis-web-reporting", "F_SQLVIEW_MANAGEMENT"]},
                            {"name": "admin user", "authorities": ["ALL"]}]
        return map(self.build_single_role, role_definitions)

    def filter_by_level(self, level):
        def filter_func(item):
            return item['level'] == level

        return filter_func

    def org_units(self):
        url = "%s/api/organisationUnits.json?fields=id,name,level&pageSize=1000" % self.url
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), headers=headers)
        org_units = json.loads(response.content)['organisationUnits']
        country_level_org_units = filter(self.filter_by_level(1), org_units)
        project_org_units = filter(self.filter_by_level(2), org_units)
        return country_level_org_units, project_org_units

    def run(self):
        country_level_org_units, project_org_units = self.org_units()
        data = {"users": self.build_user_list(country_level_org_units, project_org_units),
                "userRoles": self.create_roles()}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post("%s/api/metaData" % self.url, data=json.dumps(data),
                                 auth=HTTPBasicAuth(self.username, self.password), headers=headers)
        print response.status_code
        print response.text


def main():
    generator = UserMetaDataGenerator("users.csv", "http://localhost:8080", "admin", "district")
    generator.run()


if __name__ == '__main__':
    main()
