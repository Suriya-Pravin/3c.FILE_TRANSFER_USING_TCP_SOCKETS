
import socket
import os

HOST = '127.0.0.1'  
PORT = 65432  

def send_file(filename, conn):
    if os.path.isfile(filename):
        conn.sendall(b'EXISTS')
        file_size = os.path.getsize(filename)
        conn.sendall(str(file_size).encode('utf-8'))
        client_response = conn.recv(1024).decode('utf-8')
        if client_response == 'READY':
            with open(filename, 'rb') as f:
                chunk = f.read(1024)
                while chunk:
                    conn.sendall(chunk)
                    chunk = f.read(1024)
            print(f"File '{filename}' sent successfully.")
    else:
        conn.sendall(b'NOT_EXISTS')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"File server is listening on {HOST}:{PORT}")
    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")

            filename = conn.recv(1024).decode('utf-8')
            print(f"Client requested file: {filename}")

            send_file(filename, conn)