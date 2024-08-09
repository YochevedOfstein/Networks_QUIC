import socket
from quic import quic_send, quic_close
import time


def client_function():
    HOST = '127.0.0.1'
    PORT = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destination = (HOST, PORT)

    file_paths = [
        'file1.txt', 'file2.txt', 'file3.txt', 'file4.txt', 'file5.txt',
        'file6.txt', 'file7.txt', 'file8.txt', 'file9.txt', 'file10.txt'
    ]

    # Iterate over the files and send each one in a different stream
    for i, file_path in enumerate(file_paths, start=1):
        with open(file_path, 'rb') as file:
            data = file.read()
            quic_send(sock, destination, data, i)

    quic_close(sock, destination)


if __name__ == '__main__':
    client_function()
