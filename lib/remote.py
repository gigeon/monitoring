import socket
import cv2
import numpy as np

class Remote(object) :
    def __init__(self,logger) :
        self.logger = logger
        self.sock = None
        
    def connect(self, ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.sock = sock
            sock.connect((ip, port))
            self.logger.info(f"Start to receice image data {ip}:{port}")
            
            # 서버에서 전송한 이미지 크기 정보 수신
            length = self.recvall(self.sock, 16)
            if not length:
                self.logger.error("Failed to receive data length")
            else:
                # 받은 길이 정보를 기반으로 이미지 데이터 수신
                stringData = self.recvall(self.sock, int(length))
                if stringData:
                    data = np.frombuffer(stringData, dtype='uint8')
                    
                    # 수신한 데이터를 이미지로 디코딩 후 출력
                    decimg = cv2.imdecode(data, 1)
                    return decimg
                else:
                    self.logger.error("Failed to receive image data")
        
    # socket 수신 버퍼를 읽어서 반환하는 함수
    def recvall(self, count) :
        buf = b''
        while count:
            newbuf = self.sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf
