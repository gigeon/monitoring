import socket
import cv2
import numpy as np

# socket 수신 버퍼를 읽어서 반환하는 함수
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# 서버에 연결할 IP와 포트
TCP_IP = '128.1.1.91'
TCP_PORT = 5001

# TCP 소켓 준비 후 서버에 연결
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((TCP_IP, TCP_PORT))
    
    # 서버에서 전송한 이미지 크기 정보 수신
    length = recvall(sock, 16)
    if not length:
        print("Failed to receive data length.")
    else:
        # 받은 길이 정보를 기반으로 이미지 데이터 수신
        stringData = recvall(sock, int(length))
        if stringData:
            data = np.frombuffer(stringData, dtype='uint8')
            
            # 수신한 데이터를 이미지로 디코딩 후 출력
            decimg = cv2.imdecode(data, 1)
            cv2.imshow('CLIENT', decimg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Failed to receive image data.")