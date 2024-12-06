import asyncio
import websockets
import cv2
import numpy as np
import pyautogui
import traceback
import mss
import mss.tools

# 클라이언트 명령을 처리하는 함수
async def remote(websocket):
    print("Remote control started")
    try:
        async for data in websocket:
            print(f"Received: {data}")
            if data[0] == '1':
                if data[1] == '1':
                    result = data.split('-')
                    pyautogui.moveTo(round(float(result[1])), round(float(result[2])))
                elif data[1] == '2':
                    pyautogui.doubleClick()
                elif data[1] == '3':
                    pyautogui.doubleClick(button='right')
                elif data[1] == '4':
                    pyautogui.mouseDown()
                elif data[1] == '5':
                    pyautogui.click()
                elif data[1] == '6':
                    pyautogui.mouseDown(button='right')
                elif data[1] == '7':
                    pyautogui.click(button='right')
                elif data[1] == '8':
                    result = data.split(',')
                    pyautogui.scroll(1 if int(result[1]) > 0 else -1)
            elif data[0] == '2':
                key_mapping = {
                    "27": 'esc',
                    "2424832": 'left',
                    "2490368": 'up',
                    "2555904": 'down',
                    "2621440": 'right',
                    "8": 'backspace',
                    "9": 'tab',
                }
                key = key_mapping.get(data[1:], chr(int(data[1:])))
                pyautogui.press(key)
    except Exception as e:
        print(traceback.format_exc())


# 화면 스크린샷을 전송하는 함수
async def send_screenshot(websocket):
    try:
        while True:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)  
                img = np.array(screenshot)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
                _, imgencode = cv2.imencode('.jpg', img, encode_param)
                stringData = imgencode.tobytes()
                await websocket.send(stringData)
                await asyncio.sleep(0.2)
    except Exception as e:
        print(e)


# WebSocket 핸들러
async def handler(websocket, path):
    print("Client connected")
    await asyncio.gather(
        remote(websocket),        # 명령 처리
        send_screenshot(websocket)  # 스크린샷 전송
    )


# WebSocket 서버 시작
async def main():
    server = await websockets.serve(handler, "localhost", 5001)
    print("Server started on ws://localhost:5001")
    await server.wait_closed()


asyncio.run(main())