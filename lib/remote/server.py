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
        
        while True:
            print("1")
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # 이미지를 바이너리 형태로 변환 (인코딩)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = np.array(imgencode)
            stringData = data.tobytes()

            # 이미지의 크기 정보를 먼저 전송
            conn.send(str(len(stringData)).ljust(16).encode())
            # 이미지 데이터를 전송
            conn.send(stringData)
            