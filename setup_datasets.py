import hashlib
import requests
import json
from requests.auth import HTTPBasicAuth
from setup_users import UserMetaDataGenerator

class DataSetMetaDataGenerator(object):

    def __init__(self,url,username,password, user_data_generator):
        self.url = url
        self.username = username
        self.password = password
        self.user_data_generator = user_data_generator


    def create_id(self, value):
        return ("t%s" % hashlib.md5(value).hexdigest())[0:11]

    def create_dataset(self):
        country_level_org_units, project_org_units = self.user_data_generator.org_units()
        dataset_name = 'Some very important dataset' 
        dataset = {
            'name': dataset_name,
            'id': self.create_id(dataset_name),
            'periodType':'Weekly',
            'organisationUnits': project_org_units
        }
        return [dataset]
    
    def build_data_elements(self, prefix, count = 10):
        elements = []
        for n in range(10):
            name = '%s %d data element' % (prefix, n)
            elements.append({'name': name, 
                             'id': self.create_id(name),
                             'shortName': name,
                             'code': name,
                             'domainType': 'AGGREGATE',
                             'aggregationOperator': 'sum',
                             'type': 'int'})
        return elements
    
    def create_sections(self, dataset_id):
        first_section_data_elements = self.build_data_elements('First')
        second_section_data_elements = self.build_data_elements('Second')
        section_info = [{'name':'first section', 'elements': first_section_data_elements }, 
                        {'name':'second section', 'elements': second_section_data_elements}]
        sections = []
        for index, item in enumerate(section_info):
            name = item['name']
            sections.append({
                'name':name,
                'id':self.create_id(name),
                'displayName': name,
                'sortOrder': index + 1,
                'dataSet': {'id': dataset_id},
                'dataElements': item['elements']
            })
        return sections, first_section_data_elements + second_section_data_elements

    def run(self):
        datasets = self.create_dataset()
        sections, data_elements = self.create_sections(datasets[0]['id'])
        metadata = {
            'dataSets': datasets,
            'sections': sections,
            'dataElements': data_elements
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post("%s/api/metaData" % self.url, data=json.dumps(metadata),
                                 auth=HTTPBasicAuth(self.username, self.password), headers=headers)

        print response.content



def main():
    url = 'http://localhost:8080'
    username = 'admin'
    password = 'district'
    user_data_generator = UserMetaDataGenerator('users.csv', url,username,password)
    datasetgenerator = DataSetMetaDataGenerator(url, username, password, user_data_generator)
    datasetgenerator.run()

if __name__ == '__main__':
    main()