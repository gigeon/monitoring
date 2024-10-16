import socket
import cv2
import numpy as np
import pyautogui

# 서버에서 클라이언트로 이미지를 전송하는 코드
TCP_IP = '0.0.0.0'
TCP_PORT = 5001

# TCP 소켓 열고 클라이언트 연결 대기
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)
    print("Waiting for connection...")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected to: {addr}")
        
        # # 테스트용 코드
        # img = cv2.imread('test.png', cv2.IMREAD_COLOR)
        
        # 화면 캡처 및 cv2로 변경 (RGB -> BGR)
        screenshot = pyautogui.screenshot()
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # 이미지를 바이너리 형태로 변환 (인코딩)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imgencode = cv2.imencode('.png', img, encode_param)
        data = np.array(imgencode)
        stringData = data.tobytes()

        # 이미지의 크기 정보를 먼저 전송
        conn.send(str(len(stringData)).ljust(16).encode())
        # 이미지 데이터를 전송
        conn.send(stringData)
        print("Image sent.")