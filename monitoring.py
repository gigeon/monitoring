import logging
from lib.api import Api
from lib.detection import Detection
from lib.remote import Remote
from item import Item
import datetime

def get_month_of_week(year, month, day):
    first_day = datetime.date(year, month, 1)
    current_day = datetime.date(year, month, day)
    week_number = ((current_day.day + first_day.weekday() - 1) // 7) + 1
    return week_number

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
    
    max_check = int(api.select("SELECT MAX(CHECK_ID) AS MAX FROM `CHECK`")['MAX'])
    max_check_dtl = int(api.select("SELECT MAX(CHECK_DTL_ID) AS MAX FROM `CHECK_DTL`")['MAX']) + 1
    
    remote = Remote(logger, api)
    detection = Detection(logger, api, max_check)
    item_list = []
    
    today = datetime.datetime.today()
    
    week = get_month_of_week(today.year, today.month, today.day)
    
    device_list = api.select_all(f'select * from device')
    
    api.insert(f"""
        INSERT INTO `CHECK` VALUES(
            NEXTVAL(CHECK_SEQ),
            '{today.month}',
            '{week}',
            '{today.isoformat()}',
            'admin',
            '{today.isoformat()}',
            'admin'
    )""")
    
    for device in device_list :
        try :
            item = Item()
            item.set_device_id(device['device_id'])
            power_yn = '0'
            img = remote.connect(device['ip'],int(device['port']), max_check_dtl)
            if img is not None : 
                power_yn = '1'
                detection.version_ocr(img, item)
                item_list.append(item)
            else :
                api.insert(f"""
                    INSERT INTO
                        ERROR
                    VALUES(
                        NEXTVAL(ERROR_SEQ),
                        '{max_check_dtl}',
                        '',
                        '01',
                        '{today.isoformat()}',
                        'admin',
                        '{today.isoformat()}',
                        'admin'
                    )
                """)

            api.insert(f"""
                INSERT INTO
                    CHECK_DTL
                VALUES(
                    NEXTVAL(CHECK_DTL_SEQ),
                    '{max_check}',
                    '{item.get_device_id()}',
                    {power_yn},
                    {item.get_network_use()},
                    '{item.get_version()}',
                    '{item.get_indicator()}',
                    '{today.isoformat()}',
                    'admin',
                    '{today.isoformat()}',
                    'admin'
                )
            """)
            max_check_dtl += 1
            
        except Exception as e:
            logger.error(f"{device['device_sq_no']} Device Check Error : {e}")