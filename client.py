import socket

def create_client():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#create TCP Socket Object
    client_socket.connect(("127.0.0.1",8080))
    print("client connected")
    return client_socket

def upload_file(client_socket, file_path):
    with open(file_path,"rb") as file:
        while True:
            data=file.read(1024)
            if not data:
                print("finish sending file")
                break
            print("sending 1024 bytes...")
            client_socket.send(data)


client_socket=create_client()
upload_file(client_socket, r"C:\Users\User\Downloads\62dd3704ffd7caa73a259b82440be1ce.jpg")