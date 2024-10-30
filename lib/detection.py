import cv2
import pytesseract
from config_info import ConfigInfo
from item import Item
from lib.api import Api
import logging
import datetime

class Detection(object) :
    def __init__(self, logger: logging, api: Api, max_check):
        self.logger = logger
        self.api = api
        self.conf = ConfigInfo()
        self.max_check = max_check
        # 환경변수 설정 시 설정 필요x
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def version_ocr(self, img, item: Item):
        try : 
            self.logger.info(f"==================ocr start==================")
            errorFlag = 0
            
            ver = img[575:595, 3:60]
            ver = cv2.resize(ver, (500,200), cv2.INTER_AREA)
            ver = cv2.cvtColor(ver, cv2.COLOR_BGR2GRAY)
            ret, ver = cv2.threshold(ver, 60, 255, cv2.THRESH_BINARY)
            ver_str = pytesseract.image_to_string(
                ver, config='--psm 10 --oem 3 -c tessedit_char_whitelist=.0123456789'
            )
            item.set_version(ver_str)
        except Exception as e:
            self.logger.error(f"================== ocr error {item.get_device_id()} ==================")
            self.logger.error(e)
            errorFlag = 1
        finally :
            self.yn_detection(img, item, errorFlag)
        
    def net_ocr(self, img, item: Item, errorFlag):
        try :
            net = img[615:655, 20:40]
            net = cv2.resize(net, (500,200), cv2.INTER_AREA)
            net = cv2.cvtColor(net, cv2.COLOR_BGR2GRAY)
            ret_net, net = cv2.threshold(net, 60, 255, cv2.THRESH_BINARY)
            net_str = pytesseract.image_to_string(
                net, config='--psm 10 --oem 3 -c tessedit_char_whitelist=.0123456789'
            )
            
            item.set_version(net_str)
            
        except Exception as e:
            self.logger.error(f"================== ocr error {item.get_device_id()}==================")
            self.logger.error(e)
            errorFlag = 2
        finally :
            self.yn_detection(img, item, errorFlag)
    
    def yn_detection(self, img, item: Item, errorFlag):
        try :
            for i, _ in enumerate(self.conf.icon) :
                s = 0
                s = sum(sum(cv2.inRange(
                    img[self.conf.icon_y[i][0]:self.conf.icon_y[i][1],
                            self.conf.icon_x[i][0]:self.conf.icon_x[i][1]],
                        (0, 0, 100), (50, 50, 255)
                )))
                if s < 2000 and i == 0:
                    self.item.set_network(1)
                elif s < 2000 and i == 1:
                    self.item.set_indicator(1)
                elif s < 2000 and i == 2:
                    self.item.set_qr(1)
        except Exception as e:
            self.logger.error(f"================== ocr error {item.get_device_id()}==================")
            self.logger.error(e)
            errorFlag = 3
        finally :
            self.error(errorFlag)

    def error(self, errorFlag):
        today = datetime.datetime.today();
        if errorFlag>0:
            self.api.insert(f"""
                INSERT INTO
                    ERROR
                VALUES(
                    NEXT_VAL(ERROR_SEQ),
                    '{self.max_check}',
                    '',
                    {errorFlag},
                    '{today.isoformat()}',
                    'admin',
                    '{today.isoformat()}',
                    'admin'
                )
            """)
