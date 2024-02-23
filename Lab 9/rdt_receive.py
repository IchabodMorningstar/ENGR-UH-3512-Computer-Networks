import socket
import time
import random

IP = "127.0.0.1"
PORT = 1984
PROP_D = 0.005  # Propagation delay
P_ERROR = 0.15  # Packet error
# P_ERROR = 0
TIMEOUT = 1  # Timeout
WINDOW_SIZE = 3


# Function to handle packet reception
def receive_packet(sock):
    try:
        data, addr = sock.recvfrom(1024)
        return data.decode(), addr
    except socket.timeout:
        # Handle timeout
        return None, None


# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
sock.settimeout(TIMEOUT)

# Implement the FSM logic here
expected_sequence = 0
received_list = []

while True:
    # Receive packet
    received_data, sender_addr = receive_packet(sock)

    # Implement the rest of the receiver logic here
    if received_data:
        if received_data == "bye":
            break

        received_sequence = ord(received_data) - ord('A')
        print("\npacket", received_sequence, "received")
        if received_sequence == expected_sequence:
            # Correct packet received
            print("expected sequence number:", expected_sequence)
            char = received_data
            print("the packet data received:", char)
            expected_sequence += 1
            received_list.append(char)
            # Simulate ACK loss
            flg = random.random()
            if flg > P_ERROR:
                # Send ACK
                time.sleep(PROP_D)
                sock.sendto(str(received_sequence).encode(), sender_addr)
                print(
                    "ACK sending:", received_sequence, flg)
            else:
                print('ACK loss:', received_sequence, flg)
        else:
            # Unexpected sequence number, send the correct ACK
            time.sleep(PROP_D)
            sock.sendto(str(received_sequence).encode(), sender_addr)
            print(
                "Received packet with unexpected sequence number. Sent ACK:", received_sequence)

sock.close()
print(received_list)
