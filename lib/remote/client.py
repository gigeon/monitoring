import socket
import cv2
import numpy as np
import time

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

# 마우스 핸들링
def mouse_handling(event, x, y, flags, param):
    sock , rag = param
    if event == cv2.EVENT_MOUSEMOVE:
        sock.send(("11" + "-" + str(x/rag) + "-" + str(y/rag)).encode('utf-8'))
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        sock.send("12".encode('utf-8'))
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        sock.send("13".encode('utf-8'))
    elif event == cv2.EVENT_LBUTTONDOWN:
        sock.send(("14" + "-" + str(x/rag) + "-" + str(y/rag)).encode('utf-8'))
    elif event == cv2.EVENT_LBUTTONUP:
        sock.send("15".encode('utf-8'))
    elif event == cv2.EVENT_RBUTTONDOWN:
        sock.send(("16" + "-" + str(x/rag) + "-" + str(y/rag)).encode('utf-8'))
    elif event == cv2.EVENT_RBUTTONUP:
        sock.send("17".encode('utf-8'))
    elif event == cv2.EVENT_MOUSEWHEEL:
        sock.send(("18" + "," + str(flags)).encode('utf-8'))
        
# 서버에 연결할 IP와 포트
TCP_IP = '128.1.1.91'
# TCP_IP = 'localhost'
TCP_PORT = 5001
rag = 0.8

# TCP 소켓 준비 후 서버에 연결
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((TCP_IP, TCP_PORT))
    
    cv2.namedWindow('CLIENT')
    cv2.setMouseCallback('CLIENT', mouse_handling, param=(sock,rag))
    
    while True:
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
                
                # 원하는 사이즈로 조절
                decimg = cv2.resize(decimg, (0,0), fx=rag, fy=rag, interpolation=cv2.INTER_LINEAR)
                
                cv2.imshow('CLIENT', decimg)
                
                key = cv2.waitKeyEx(1)
                print(key)
                if key > 0 :
                    sock.send(("2" + str(key)).encode('utf-8'))
                
                # 종료 이벤트 'ESC'
                # if key == 27 :
                #     break
                
                time.sleep(0.01)
            else:
                print("Failed to receive image data.")
                break
    cv2.destroyAllWindows()