import cv2
import pytesseract
from config_info import ConfigInfo
from item import Item

class Detection(object) :
    def __init__(self, logger):
        self.logger = logger
        self.conf = ConfigInfo()
        self.item = Item()
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def ocr(self, img):
        if img is not None :
            self.logger.info(f"==================ocr start==================")
            try :
                ver = img[575:595, 3:60]
                ver = cv2.resize(ver, (500,200), cv2.INTER_AREA)
                
                ver = cv2.cvtColor(ver, cv2.COLOR_BGR2GRAY)
                ret, ver = cv2.threshold(ver, 60, 255, cv2.THRESH_BINARY)

                string = pytesseract.image_to_string(
                    ver, config='--psm 10 --oem 3 -c tessedit_char_whitelist=.0123456789'
                )
                print(string)
                
            except Exception as e:
                self.logger.error(f"==================ocr error==================")
                # 실패처리
        else :
            self.logger.error(f"==================ocr error==================")
                # 실패처리
    
    def yn_detection(self, img):
        if img is not None :
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
                self.logger.error(f"==================ocr error==================")
                self.logger.error(e)
                # 실패처리
        else :            
            self.logger.error(f"==================ocr error==================")
                # 실패처리
