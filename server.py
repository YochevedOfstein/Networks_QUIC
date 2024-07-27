import socket
from quic import quic_recv, quic_close, print_statistics


def server_function():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 10000))

    print("Server listening")
    stream_ids = list(range(1, 11))

    while True:
        try:
            for stream_id in stream_ids:
                quic_recv(sock)
        except Exception as e:
            print(f"Error receiving packet: {e}")
            break

    quic_close(sock, ('localhost', 10000))


if __name__ == '__main__':
    server_function()
