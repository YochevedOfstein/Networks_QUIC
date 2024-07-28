import struct
import socket
import random
import time

stream_packet_sizes = {}
stream_statistics = {}

def set_stream_packet_size(stream_id):
    if stream_id not in stream_packet_sizes:
        packet_size = random.randint(1000, 2000)
        stream_packet_sizes[stream_id] = packet_size
        stream_statistics[stream_id] = {'bytes': 0, 'packets': 0, 'start_time': None, 'end_time': None}
    return stream_packet_sizes[stream_id]

def create_quic_packet(stream_id, sequence_number, data):
    packet_size = set_stream_packet_size(stream_id)
    data = data[:packet_size]
    packet_format = f'I I H {packet_size}s'
    packet = struct.pack(packet_format, stream_id, sequence_number, len(data), data)
    return packet

def parse_quic_packet(packet):
    header_format = 'I I H'
    header_size = struct.calcsize(header_format)
    try:
        stream_id, frame_offset, payload_length = struct.unpack(header_format, packet[:header_size])
        data_format = f'{payload_length}s'
        data = struct.unpack(data_format, packet[header_size:header_size + payload_length])[0]
        return stream_id, frame_offset, data
    except struct.error as e:
        print(f"Error parsing packet: {e}")
        print(f"Packet length: {len(packet)}, Expected header size: {header_size}")
        return None, None, None

def quic_send(data, destination, sock, stream_id):
    frame_offset = 0
    if stream_id not in stream_statistics:
        stream_statistics[stream_id] = {'bytes': 0, 'packets': 0, 'start_time': None, 'end_time': None}
    while data:
        packet = create_quic_packet(stream_id, frame_offset, data)
        if stream_statistics[stream_id]['start_time'] is None:
            stream_statistics[stream_id]['start_time'] = time.time()
        sock.sendto(packet, destination)
        stream_statistics[stream_id]['bytes'] += len(data[:stream_packet_sizes[stream_id]])
        stream_statistics[stream_id]['packets'] += 1
        stream_statistics[stream_id]['end_time'] = time.time()
        frame_offset += len(data[:stream_packet_sizes[stream_id]])
        data = data[stream_packet_sizes[stream_id]:]
        print(f"Sent packet to {destination} with size {len(packet)} bytes for stream {stream_id}, frame offset {frame_offset}")

def quic_recv(sock):
    packet, _ = sock.recvfrom(2048)
    if packet == b"close":
        print("Received close packet")
        return "close", None, None

    stream_id, frame_offset, data = parse_quic_packet(packet)
    if stream_id is None:
        print(f"Received invalid packet: {packet}")
        return

    if stream_id not in stream_statistics:
        stream_statistics[stream_id] = {'bytes': 0, 'packets': 0, 'start_time': None, 'end_time': None}

    if stream_statistics[stream_id]['start_time'] is None:
        stream_statistics[stream_id]['start_time'] = time.time()
    stream_statistics[stream_id]['bytes'] += len(data)
    stream_statistics[stream_id]['packets'] += 1
    stream_statistics[stream_id]['end_time'] = time.time()
    print(f"Received packet from stream {stream_id}, frame offset {frame_offset}, data: {data.decode()}")
    return stream_id, frame_offset, data

def quic_close(sock, destination):
    try:
        sock.sendto(b"close", destination)
        sock.close()
        print("QUIC connection closed")
    except socket.error as e:
        print(f"Socket error: {e}")

def print_statistics():
    for stream_id, stats in stream_statistics.items():
        total_bytes = stats['bytes']
        total_packets = stats['packets']
        start_time = stats['start_time']
        end_time = stats['end_time']
        duration = end_time - start_time if end_time and start_time else 0
        data_rate = total_bytes / duration if duration > 0 else 0
        packet_rate = total_packets / duration if duration > 0 else 0
        print(f"Stream {stream_id}:")
        print(f"\tTotal bytes: {total_bytes}")
        print(f"\tTotal packets: {total_packets}")
        print(f"\tData rate: {data_rate:.2f} bytes/sec")
        print(f"\tPacket rate: {packet_rate:.2f} packets/sec")

    total_bytes = sum(stats['bytes'] for stats in stream_statistics.values())
    total_packets = sum(stats['packets'] for stats in stream_statistics.values())
    total_duration = max((stats['end_time'] - stats['start_time']) for stats in stream_statistics.values() if stats['end_time'] and stats['start_time'])
    total_data_rate = total_bytes / total_duration if total_duration > 0 else 0
    total_packet_rate = total_packets / total_duration if total_duration > 0 else 0

    print("Overall statistics:")
    print(f"\tTotal bytes: {total_bytes}")
    print(f"\tTotal packets: {total_packets}")
    print(f"\tData rate: {total_data_rate:.2f} bytes/sec")
    print(f"\tPacket rate: {total_packet_rate:.2f} packets/sec")
