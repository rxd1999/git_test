import socket
import sys
import time


class Server:
    def __init__(self) -> None:
        self.my_socket = socket.socket()
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.my_socket.bind(('0.0.0.0', 8000))
            self.my_socket.listen()
        except:
            pass

    def connect(self):
        self.client_socket, _ = self.my_socket.accept()
    
    def send(self, msg: str):
        self.client_socket.send(msg.encode())

    def recv(self)-> str:
        return self.client_socket.recv(1024).decode()
    
    def close(self):
        self.client_socket.close()

class Client:
    def __init__(self) -> None:
        pass
    
    def connect(self, ip: str, port: int):
        self.my_socket = socket.socket()
        self.my_socket.connect((ip, port))
    
    def send(self, msg: str):
        self.my_socket.send(msg.encode())
    
    def recv(self):
        return self.my_socket.recv(1024).decode()
    
    def close(self):
        self.my_socket.close()
    
if sys.platform == 'win32':
    communicator = Client()
    def start(ip: str, port: int = 8000):
        communicator.connect(ip, port)
    
    def win_ok():
        communicator.send('ok')
    
    def wait_linux():
        msg = communicator.recv()
        assert msg == 'ok', f"should recv ok, but got {msg}"
    
    def is_end()-> bool:
        msg = communicator.recv()
        if  msg == 'end':
            time.sleep(3)
            communicator.close()
            return True
        return False
    
if sys.platform == 'linux':
    communicator = Server()
    def start():
        communicator.connect()
    
    def linux_ok():
        communicator.send('ok')
        
    def wait_win():
        msg = communicator.recv()
        assert msg == 'ok', f"should recv ok, but got {msg}"

    def end():
        communicator.send('end')



