import requests
import logging

logger = logging.getLogger(name="monitoring_log")

class Api(object) :
    def __init__(self, logger):
        self.def_url = "localhost:5678"
        self.logger = logger
        
    def api_get(self, url, param):
        response = requests.get(self.def_url + url, params = param, verify=False)
        if response.status_code != 200 :
            logger.error(f' \
                        status : {response.status_code}, \
                        message : {response.text} \
                        ')
            return
        return response.json()
        
    def api_post(self, url, param):
        response = requests.post(self.def_url + url, params = param, verify=False)
        if response.status_code != 200 :
            return
        return response.json()
    