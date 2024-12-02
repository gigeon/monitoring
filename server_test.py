import asyncio
import websockets
import cv2
import numpy as np
import time

# 서버에서 클라이언트로 이미지를 전송하는 코드
TCP_IP = '0.0.0.0'
TCP_PORT = 5001

async def handler(websocket, path):
    print("Client connected")
    try :
        while True:
            screenshot = cv2.imread('test.jpg', cv2.IMREAD_COLOR)
            img = np.array(screenshot)
            
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, imgencode = cv2.imencode('.png', img, encode_param)
            data = np.array(imgencode)
            stringData = data.tobytes()
            
            await websocket.send(stringData)
            time.sleep(1)
    except Exception as e:
        print(e)

async def main():
    server = await websockets.serve(handler, "localhost", 5001)
    print("Server started on ws://localhost:5001")
    await server.wait_closed()

asyncio.run(main())