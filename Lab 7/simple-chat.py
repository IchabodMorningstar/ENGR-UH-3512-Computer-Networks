import socket
import threading
import select
import sys


# Function for sending messages
def send_msg():
    while True:
        msg = input()
        if msg:
            try:
                if msg == "exit":
                    # print('ready to exit')
                    receiver_address = peers[username]
                    client_socket = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect(receiver_address)
                    client_socket.send(msg.encode())
                    client_socket.close()
                    # print('breaking send')
                    break
                else:
                    # Split input into receiver and message
                    receiver, text = msg.split(">", 1)
                    # Check and send message to the receiver
                    if receiver in peers:
                        try:
                            receiver_address = peers[receiver]
                            client_socket = socket.socket(
                                socket.AF_INET, socket.SOCK_STREAM)
                            client_socket.connect(receiver_address)
                            client_socket.send(text.encode())
                            client_socket.close()
                        except:
                            print('user not online')
                    else:
                        print("Receiver not found in the peer list.")
            except ValueError:
                print("Invalid message format. Please use 'Username>Message'.")


# Function for receiving messages
def receive_msg():
    stop_flag = False
    # Receiving the messages
    while True and not stop_flag:
        sockets_list = [server_socket]
        sockets_list.extend(client_sockets)

        read_sockets, _, _ = select.select(sockets_list, [], [])

        for sock in read_sockets:
            if sock == server_socket:
                client_socket, _ = server_socket.accept()
                client_sockets.append(client_socket)
            else:
                message = sock.recv(1024).decode()
                if not message:
                    sock.close()
                    client_sockets.remove(sock)
                else:
                    if message == "exit":
                        # To exit
                        stop_flag = True
                    else:
                        # Decoding the messages
                        sender_ip = sock.getpeername()[0]
                        for i in peers.keys():
                            if sender_ip == peers[i][0]:
                                sender = i
                        print(sender + ": " + message)


if __name__ == "__main__":
    peers = {
        "as12106": ("10.225.2.94", 5000),
        "ae2200": ("10.225.26.197", 5001),
        "bz1224": ("10.224.17.149", 5002),
        "kka280": ("10.225.50.130", 5003),
        # "ome2005": ("?", 5004),
        # "pk2269": ("?", 5005),
        # "nm3749": ("?", 5006),
        "zz3848": ("10.225.15.190", 5007),
        "cc7486": ("10.225.35.127", 5008),
        "js12556": ("10.225.1.21", 5009),
        "ccl": ("10.224.17.239", 1112)
    }

    # Create current user as a server
    username = input("what is your username?\n")

    # Create the user as both client and server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_IP = peers[username][0]
    SERVER_PORT = peers[username][1]
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)

    client_sockets = []

    sending = threading.Thread(target=send_msg)
    receiving = threading.Thread(target=receive_msg)

    # Start threading
    sending.start()
    receiving.start()

    print(f"Welcome {username}! Type 'exit' to leave")

    # Terminate threading
    sending.join()
    receiving.join()

    server_socket.close()
    sys.exit()
