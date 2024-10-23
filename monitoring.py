from vncdotool import api
import logging
import lib.api as Api
from lib.detection import Detection
import cv2

if __name__ == "__main__" :
    
    logger = logging.getLogger(name="monitoring")
    logger.setLevel(logging.INFO)
    
    file_handler = logging.FileHandler("monitoring.log")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.info("==================Monitoring Start==================")

    # 원격제어 테스트 시 주석처리
    api = Api(logger)
    
    device_list = api.select(f'select * from device')
    
    print(device_list)