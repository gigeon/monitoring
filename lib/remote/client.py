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

# 마우스 핸들링
def mouse_handling(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print(x,"==", y)
        param.send(("1" + "-" + str(x) + "-" + str(y)).encode('utf-8'))
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        print("left",x,"==", y)
        param.send("2".encode('utf-8'))
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        print("right",x,"==", y)
        param.send("3".encode('utf-8'))
        
# 서버에 연결할 IP와 포트
TCP_IP = '128.1.1.91'
# TCP_IP = 'localhost'
TCP_PORT = 5001



# TCP 소켓 준비 후 서버에 연결
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((TCP_IP, TCP_PORT))
    
    cv2.namedWindow('CLIENT')
    cv2.setMouseCallback('CLIENT', mouse_handling, param=sock)

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
                cv2.imshow('CLIENT', decimg)
                
                if cv2.waitKey(1) == 27 :
                    break
            else:
                print("Failed to receive image data.")
                break
    cv2.destroyAllWindows()