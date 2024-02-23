import socket
import threading
import select
import random
import ast
import sys


# Function for sending process
def sends(msg):
    if msg:
        try:
            # Split input into receiver and message
            receiver, text = msg.split(">", 1)
            addr = str(peers[username])
            text += ">" + username + "!" + addr
            # Check and send message to the receiver
            if receiver in peers:
                receiver_address = peers[receiver]
                client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(receiver_address)
                client_socket.send(text.encode())
                client_socket.close()
            else:
                print("Receiver not found in the peer list.")
        except ValueError:
            print("Invalid message format. Please use 'Username>Message'.")


# Function for Exiting
def exits():
    # Telling others about exiting
    lst = list(friends)
    for i in lst:
        msg = i + ">exiting#now"
        try:
            sends(msg)
        except:
            pass


# Function for sending messages
def send_msg():
    while True:
        message = input()
        if message == "exit":
            exits()
            break
        else:
            sends(message)


# Function for receiving messages
def receive_msg():
    # Flag to help killing this thread
    receive_flg = True

    # Receiving the messages
    while receive_flg:
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
                    # Decoding the messages
                    message, sender = message.split(">")
                    sender, addr = sender.split("!")

                    # A user not known before
                    if sender not in peers.keys():
                        peers[sender] = ast.literal_eval(addr)
                        msg = sender + ">peer#update" + str(new_user)
                        sends(msg)
                        new_user[sender] = peers[sender]

                    # A user not talked before
                    if sender not in friends and not message.startswith("exiting#now"):
                        friends.append(sender)

                    # New user registering message
                    if message.startswith("new#user#here"):
                        message = message[13:]
                        tpl = tuple(message[1:-1].split(","))
                        tpl = (tpl[0], int(tpl[1]))
                        peers[sender] = tpl
                    # Update peers list message
                    elif message.startswith("peer#update"):
                        new_peer = ast.literal_eval(message[11:])
                        # print(f"received list from {sender}: {new_peer}")
                        peers.update(new_peer)
                        friends.extend(
                            item for item in new_peer.keys() if item not in friends)
                    # Peer exiting message
                    elif message.startswith("exiting#now"):
                        if sender != username:
                            print(f"User {sender} has logged off")
                            friends.remove(sender)
                        else:
                            receive_flg = False
                            print("See you next time")
                    # Chatting message
                    else:
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
        "cc7486": ("10.224.17.239", 5008),
        "js12556": ("10.225.1.21", 5009),
        "ccl": ("10.225.35.127", 1112),
        "max": ("10.225.35.127", 1012),
        "john": ("10.225.35.127", 1102)
    }

    # Create current user as a server
    username = input("what is your username?\n")

    # Check if the user exists
    if username not in peers.keys():
        ipadd = socket.gethostbyname(socket.gethostname())
        portadd = random.randint(1000, 9999)
        addr = (ipadd, portadd)
        peers[username] = addr
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER_IP = peers[username][0]
        SERVER_PORT = peers[username][1]
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(5)
    else:
        # Create the user as both client and server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER_IP = peers[username][0]
        SERVER_PORT = peers[username][1]
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(5)

    print(f"Welcome {username}! Leaving by typing 'exit'")

    new_user = {}

    friends = [username]

    client_sockets = []

    sending = threading.Thread(target=send_msg)
    receiving = threading.Thread(target=receive_msg)

    sending.start()
    receiving.start()

    # Killing threads
    sending.join()
    receiving.join()

    # Closing socket and terminate programme
    server_socket.close()
    sys.exit()
