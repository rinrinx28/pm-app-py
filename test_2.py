import socket

def start_client():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('localhost', 12345))
    client_sock.sendall(b"Hello from client!")
    client_sock.close()

if __name__ == "__main__":
    start_client()
