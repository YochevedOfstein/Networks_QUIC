import socket
from quic import quic_send, quic_close
import time


def client_function():
    Number_Of_Streams = 10
    HOST = '127.0.0.1'
    PORT = 5060
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destination = (HOST, PORT)

    file_paths = [
        'file1.txt', 'file2.txt', 'file3.txt', 'file4.txt', 'file5.txt',
        'file6.txt', 'file7.txt', 'file8.txt', 'file9.txt', 'file10.txt'
    ]

    for i in range(Number_Of_Streams):
        file_path = file_paths[i%10]
        with open(file_path, 'rb') as file:
            data = file.read()
            quic_send(sock, destination, data, i+1)

    quic_close(sock, destination)


if __name__ == '__main__':
    client_function()
