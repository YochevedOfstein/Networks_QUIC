import socket
from quic import quic_recv, quic_close, print_statistics

def server_function():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 10000))

    print("Server listening")
    stream_ids = list(range(1, 11))

    try:
        while True:
            for stream_id in stream_ids:
                result = quic_recv(sock)
                if result == "close":
                    break
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error receiving packet: {e}")

    quic_close(sock, ('localhost', 10000))
    print_statistics()

if __name__ == '__main__':
    server_function()
