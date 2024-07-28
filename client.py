import socket
from quic import quic_send, quic_close

def client_function():
    HOST = '127.0.0.1'
    PORT = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destination = (HOST, PORT)
    stream_ids = list(range(1, 11))
    data = b"Hello this is client data" * 100

    for stream_id in stream_ids:
        quic_send(data, destination, sock, stream_id)

    quic_close(sock, destination)

if __name__ == '__main__':
    client_function()
