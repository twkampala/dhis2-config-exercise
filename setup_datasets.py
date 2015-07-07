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
            'shortName': dataset_name,
            'organisationUnits': project_org_units
        }
        return [dataset]
    
    def build_data_elements(self, prefix, combo, count = 10):
        elements = []
        for n in range(10):
            name = '%s %d data element' % (prefix, n)
            elements.append({'name': name, 
                             'id': self.create_id(name),
                             'shortName': name,
                             'code': name,
                             'domainType': 'AGGREGATE',
                             'aggregationOperator': 'sum',
                             'categoryCombo': combo,
                             'type': 'int'})
        return elements
    
    def create_sections(self, dataset_id,age_sex_combo, migration_arrival_combo):
        first_section_data_elements = self.build_data_elements('First', age_sex_combo)
        second_section_data_elements = self.build_data_elements('Second', migration_arrival_combo)
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

    def build_migration_arrival_categories(self):
        first_cat_name = 'migration'
        migration_options = [{'name': 'RESIDENT', 'id': self.create_id('RESIDENT'),'shortName': 'RESIDENT', 'code': 'RESIDENT'},
                       {'name': 'REFUGEE', 'id': self.create_id('REFUGEE'),'shortName': 'REFUGEE', 'code': 'REFUGEE'}]
        arrival_options = [{'name': 'ALIVE', 'id': self.create_id('ALIVE'),'shortName': 'ALIVE', 'code': 'ALIVE'},
                       {'name': 'DEAD', 'id': self.create_id('DEAD'),'shortName': 'DEAD', 'code': 'DEAD'}]
        second_cat_name = 'arrival'
        return [{
                 'name': first_cat_name, 
                 'id': self.create_id(first_cat_name), 
                 'shortName': first_cat_name,
                 'categoryOptions': migration_options
                }, {
                'name': second_cat_name,
                'id': self.create_id(second_cat_name),
                'shortName': second_cat_name,
                'categoryOptions': arrival_options
                }], migration_options + arrival_options

    def build_age_sex_categories(self):
        first_cat_name = 'Some Age'
        age_options = [{'name': 'OLD', 'id': self.create_id('OLD'),'shortName': 'OLD', 'code': 'OLD'},
                       {'name': 'YOUNG', 'id': self.create_id('YOUNG'),'shortName': 'YOUNG', 'code': 'YOUNG'}]
        sex_options = [{'name': 'MALE', 'id': self.create_id('MALE'),'shortName': 'MALE', 'code': 'MALE'},
                       {'name': 'FEMALE', 'id': self.create_id('FEMALE'),'shortName': 'FEMALE', 'code': 'FEMALE'}]
        second_cat_name = 'Some Sex'
        return [{
                 'name': first_cat_name, 
                 'id': self.create_id(first_cat_name), 
                 'shortName': first_cat_name,
                 'categoryOptions': age_options
                }, {
                'name': second_cat_name,
                'id': self.create_id(second_cat_name),
                'shortName': second_cat_name,
                'categoryOptions': sex_options
                }], age_options + sex_options
    
    def build_combo(self, name, categories, options):
        return {'name': name, 'id': self.create_id(name), 'categories': categories, 'categoryOptionCombos': options}
    
    def run(self):
        datasets = self.create_dataset()
        age_sex_categories, category_options = self.build_age_sex_categories()
        age_sex_combo = self.build_combo('Some Age and Sex', age_sex_categories, category_options)
        migration_arrival_categories, migration_category_options = self.build_migration_arrival_categories()
        migration_arrival_combo = self.build_combo('Migration and Arrival', migration_arrival_categories, migration_category_options)
        sections, data_elements = self.create_sections(datasets[0]['id'], age_sex_combo, migration_arrival_combo)
        datasets[0]['dataElements'] = data_elements
        metadata = {
            'dataSets': datasets,
            'sections': sections,
            'dataElements': data_elements,
            'categories' : age_sex_categories + migration_arrival_categories,
            'categoryOptions': category_options + migration_category_options,
            'categoryOptionCombos': category_options + migration_category_options,
            'categoryCombos': [age_sex_combo, migration_arrival_combo],
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