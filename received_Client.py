import socket

HOST = '127.0.0.1'  
PORT = 65432  


def receive_file(filename, conn):
    response = conn.recv(1024).decode('utf-8')

    if response == 'EXISTS':
        file_size = int(conn.recv(1024).decode('utf-8'))
        print(f"File '{filename}' exists on server, size: {file_size} bytes.")

        conn.sendall(b'READY')

        with open('received_' + filename, 'wb') as f:
            total_received = 0
            while total_received < file_size:
                data = conn.recv(1024)
                f.write(data)
                total_received += len(data)
                print(f"Received {total_received} of {file_size} bytes")

        print(f"File '{filename}' received and saved as 'received_{filename}'")
    else:
        print("File does not exist on the server.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    filename = input("Enter the filename you want to download: ")
    client_socket.sendall(filename.encode('utf-8'))

    receive_file(filename, client_socket)