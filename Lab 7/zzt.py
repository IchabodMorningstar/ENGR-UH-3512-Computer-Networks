import socket
import threading
import ast


# Function to receive and display messages
def receive_messages():
    while True:
        conn, addr = listen_socket.accept()
        # print("accepted")
        message = conn.recv(1024).decode('utf-8')
        if not message:
            break
        if 'New user:' in message:
            print(message)
            name_fin = message.index('!')
            address_start = message.index('[')
            new_ip = message[address_start+1:message.index(",")]
            new_port = int(message[message.index(",")+1:-1])
            peer_sockets[message[10:name_fin]] = [new_ip, new_port]
            # print("1:",peer_sockets)
            # print("2:",peer_sockets[message[10:name_fin]])
            if connect_to_peer_with_timeout(message[10:name_fin], new_ip, new_port, 1):
                # print("conn1")
                target_socket = peer_sockets_c.get(message[10:name_fin])
                if target_socket:
                    peer_message = 'Peers:' + str(peer_sockets)
                    # pickled_data = pickle.dumps(peer_sockets)
                    target_socket.send(peer_message.encode('utf-8'))
        elif "Peers:" in message:
            print(message)
            full = ast.literal_eval(message[6:])
            for i in full.keys():
                if i not in peer_sockets.keys():
                    peer_sockets[i] = full[i]
        elif message == 'exit':
            sender = addr[0]
            hostname = socket.gethostname()
            my_ip = socket.gethostbyname(hostname)
            if sender == my_ip:
                break
            else:
                for i in peer_sockets.keys():
                    if peer_sockets[i][0] == sender:
                        username = i
                print(f'user {username} has logged off')
                # del peer_sockets_c[username]
                conn.close()
        else:
            sender = addr[0]
            for i in peer_sockets.keys():
                if peer_sockets[i][0] == sender:
                    message = i + ':' + message
            print(message)


# Function to send messages to a specific peer
def send_message():
    while True:
        message = input("")
        try:
            index = message.index(">")
            peer_username = message[:index]
            message = message[index+1:]
            if peer_username in peer_sockets:
                connect_to_peer(
                    peer_username, peer_sockets[peer_username][0], peer_sockets[peer_username][1])
                # print("conn2")
                target_socket = peer_sockets_c.get(peer_username)
                if target_socket:
                    target_socket.send(message.encode('utf-8'))
                    # print("Message sent")
                else:
                    print(f"User '{peer_username}' is not online.")
        except ValueError:
            if message == 'exit':
                for i in peer_sockets.keys():
                    # connect_to_peer(i, peer_sockets[i][0], peer_sockets[i][1])
                    if connect_to_peer_with_timeout(i, peer_sockets[i][0], peer_sockets[i][1], 0.5):
                        # print("conn3")
                        target_socket = peer_sockets_c.get(i)
                        if target_socket:
                            target_socket.send(message.encode('utf-8'))
                    else:
                        continue
                break


# Function to connect to a peer
def connect_to_peer(peer_username, peer_ip, peer_port):
    try:
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((peer_ip, peer_port))
        peer_sockets_c[peer_username] = peer_socket

    except ConnectionRefusedError:
        print(
            f"Failed to connect to user '{peer_username}' at {peer_ip}:{peer_port}")


def connect_to_peer_with_timeout(peer_username, peer_ip, peer_port, timeout):
    try:
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        peer_socket.settimeout(timeout)
        peer_socket.connect((peer_ip, peer_port))
        peer_sockets_c[peer_username] = peer_socket
        return True
    except socket.timeout:
        print(
            f"Connection to user '{peer_username}' at {peer_ip}:{peer_port} timed out.")
    except ConnectionRefusedError:
        print(
            f"Failed to connect to user '{peer_username}' at {peer_ip}:{peer_port}")
    return False


# Create a dictionary to store peer sockets
# peer_sockets = {'zza': ['10.225.15.190', 8801], 'zzb': [
#     '10.225.15.190', 8802], 'zzc': ['10.225.15.190', 8003]}
peer_sockets = {'as12106': ['10.225.2.94', 5000], 'ae2200': ['10.225.26.197', 5001], 'bz1224': ['10.224.17.149', 5002], 'kka280': [
    '10.225.50.130', 5003], 'zz3848': ['10.225.15.190', 5007], 'cc7486': ['10.225.35.127', 5008], 'js12556': ['10.225.1.21', 5009],
    "ccl": ["10.225.35.127", 1112]}
peer_sockets_c = {}

# Constants for this peer
username = input('Username>')
if username in peer_sockets.keys():
    HOST = peer_sockets[username][0]
    PORT = peer_sockets[username][1]
else:
    user_ip = input("Enter your IP address: ")
    user_port = int(input("Enter your port number: "))
    peer_sockets[username] = [user_ip, user_port]
    # print(peer_sockets)
    print(f"User '{username}' signed up.")
    for user in peer_sockets.keys():
        if user != username:
            if connect_to_peer_with_timeout(user, peer_sockets[user][0], peer_sockets[user][1], 0.5):
                # print("conn4")
                target_socket = peer_sockets_c.get(user)
                if target_socket:
                    new_user_info = f"New user: {username}! at [{user_ip},{user_port}]"
                    target_socket.send(new_user_info.encode('utf-8'))
                    HOST = user_ip  # str
                    PORT = user_port  # int
            else:
                continue

# Create a socket for this peer
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind((HOST, PORT))
listen_socket.listen()

send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_messages)
send_thread.start()
receive_thread.start()
send_thread.join()
receive_thread.join()

listen_socket.close()
