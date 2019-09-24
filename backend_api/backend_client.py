import requests
import yaml
import os


class AMSClient:
    def __init__(self):
        with open('config.yaml') as cfg_file:
            cfg = yaml.load(cfg_file, Loader=yaml.Loader).get(os.environ['ENV'])
            self.ams_service = cfg.get('ams-service')
            self.ams_key = cfg.get('ams-key')
            self.headers = {
                'Authorization': f'Bearer {self.ams_key}'
            }

    def get(self, url):
        resp = requests.get(f'{self.ams_service}{url}', headers=self.headers)
        return resp.status_code, resp.json()

    def get_file(self, url):
        resp = requests.get(f'{self.ams_service}{url}', headers=self.headers, stream=True)
        return resp

    def post(self, url, payload, files=None):
        resp = requests.post(f'{self.ams_service}{url}', headers=self.headers, data=payload, files=files)
        return resp.status_code, resp.json()

    def patch(self, url, payload):
        resp = requests.patch(f'{self.ams_service}{url}', headers=self.headers, data=payload)
        return resp.status_code, resp.json()
