import logging
from lib.api import Api
from lib.detection import Detection
from lib.remote import Remote

if __name__ == "__main__" :
    logger = logging.getLogger(name="monitoring")
    logger.setLevel(logging.INFO)
    
    file_handler = logging.FileHandler("monitoring.log")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.info("==================Monitoring Start==================")

    api = Api(logger)
    remote = Remote(logger)
    device_list = api.select(f'select * from device')
    
    for device in device_list :
        remote.connect(device['ip'],device['port'])
    
    print(device_list)