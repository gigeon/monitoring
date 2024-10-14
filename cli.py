import socket
import os
from PIL import Image
import io

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    while True:
        command = input("Enter command (or 'exit' to quit): ")
        client_socket.send(command.encode())
        
        if command.lower() == 'exit':
            print("Exiting...")
            break
        
        if command.lower() == 'screenshot':
            # 이미지 데이터 수신
            header = client_socket.recv(4)
            if header.startswith(b'IMAGE'):
                length = int.from_bytes(header[6:], 'little')  # 이미지 길이
                img_data = bytearray()
                
                while len(img_data) < length:
                    img_data.extend(client_socket.recv(length - len(img_data)))

                # 이미지 저장 및 보기
                img = Image.open(io.BytesIO(img_data))
                img.show()
            else:
                output = client_socket.recv(4096).decode()
                print(output)
        else:
            # Receive the output from the server
            output = client_socket.recv(4096).decode()
            print(output)
    
    client_socket.close()

if __name__ == "__main__":
    server_ip = '128.1.1.91'
    server_port = int(input("Enter server port: "))
    start_client(server_ip, server_port)