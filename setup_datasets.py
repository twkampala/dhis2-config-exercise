import hashlib
import requests
import json
from requests.auth import HTTPBasicAuth

class DataSetMetaDataGenerator(object):

    def __init__(self,url,username,password):
        self.url = url
        self.username = username
        self.password = password


    def create_id(self, value):
        return ("t%s" % hashlib.md5(value).hexdigest())[0:11]

    def create_dataset(self):
        dataset_name = 'Some very important dataset' 
        dataset = {
            'name': dataset_name,
            'id': self.create_id(dataset_name),
            'periodType':'Weekly',
        }

        metadata = {
            'dataSets': [dataset]
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post("%s/api/metaData" % self.url, data=json.dumps(metadata),
                                 auth=HTTPBasicAuth(self.username, self.password), headers=headers)

        print response.content

    def run(self):
        self.create_dataset()


def main():
    url = 'http://localhost:8080'
    username = 'admin'
    password = 'district'
    datasetgenerator = DataSetMetaDataGenerator(url,username,password)
    datasetgenerator.run()

if __name__ == '__main__':
    main()