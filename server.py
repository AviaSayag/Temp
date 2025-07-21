import socket


def create_server():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#create TCP Socket Object
    server_socket.bind(("127.0.0.1",8080))
    server_socket.listen(5)
    print(f"Listening for new connections")
    return server_socket

def accept_client(server_socket):
    client_socket, client_adress= server_socket.accept()
    print(f"Connection established with {client_adress}")
    return client_socket


def download_file(client_socket, file_path):
    with open(file_path,"wb") as file:
        while True:
            data=client_socket.recv(1024)
            if not data:
                print("file finished")
                break
            print("recived 1024 bytes")
            file.write(data)


server_sock =create_server()
client_sock = accept_client(server_sock)
download_file(client_sock,"avia.jpg")