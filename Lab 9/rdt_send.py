import socket
import time
import random

# Constants
UDP_IP = "127.0.0.1"
UDP_PORT = 1984
BUFFER_SIZE = 1024
PROP_D = 0.005  # Propagation delay in milliseconds
P_ERROR = 0.15  # Packet error rate
# P_ERROR = 0
TIMEOUT = 1
WINDOW_SIZE = 3
msg = [chr(ord('A') + i) for i in range(8)] + ['-1'] * 10


# Function to handle packet sending
def send_packet(sock, data, addr):
    # Implement the logic for introducing errors here
    p = random.uniform(0, 1)
    if p > P_ERROR or data == "bye".encode():
        # Send packet
        time.sleep(PROP_D)
        sock.sendto(data, addr)
    else:
        print('Packet is lost', data, p)


# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

# Implement the FSM logic here
base = 0
next_sequence = 0

while base < 8:
    while next_sequence < base + WINDOW_SIZE and next_sequence < 8:
        # Implement the rest of the sender logic here
        packet_data = msg[next_sequence].encode()
        print("the sequence number of the packet being sent:", next_sequence)

        send_packet(sock, packet_data, (UDP_IP, UDP_PORT))
        next_sequence += 1

    # print("next sequence", next_sequence)
    try:
        while True:
            # Wait for ACK
            ack_data, _ = sock.recvfrom(BUFFER_SIZE)
            ack_sequence = int(ack_data.decode())
            print("ACK received for sequence number:", ack_sequence)

            if ack_sequence == base:
                base += 1
                if next_sequence < base + WINDOW_SIZE and next_sequence < 8:
                    print("the sequence number of the packet being sent:",
                          next_sequence)
                    send_packet(
                        sock, msg[next_sequence].encode(), (UDP_IP, UDP_PORT))
                    next_sequence += 1
            else:
                break

    except socket.timeout:
        if base < 8:
            print('\nTime out occured for packet', base)
            next_sequence = base


packet_data = "bye"
send_packet(sock, packet_data.encode(), (UDP_IP, UDP_PORT))
sock.close()
