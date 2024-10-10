from vncdotool import api
import logging
import lib.api as Api

if __name__ == "__main__" :
    
    logger = logging.getLogger(name="monitoring")
    logger.setLevel(logging.INFO)
    
    file_handler = logging.FileHandler("monitoring.log")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.info("==================Monitoring Start==================")

    # 접속 정보 (DB에서 끌고오는걸로 변경 예정)
    server_ip = "10.0.2.15"
    server_port = ""
    server_pwd = ""
    db_url = ""
    
    # 원격제어 테스트 시 주석처리
    api = Api(logger)
    
    result = api.get("/deviceList")

    client = api.connect(f"{server_ip}::{server_port}", password=server_pwd)

    client.captureScreen("test_screenshot.png")

    # 클라이언트 연결 종료
    client.disconnect()