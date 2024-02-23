import socket
import sys

# 'localhost' used as a bind IP address since I am not connecting 
host = 'localhost'

# Not really necessary, but it used to specify which port to bind to
if len(sys.argv) == 2:
    port = int(sys.argv[1])
else:
    port = 8080

# Instantiating a socket object
# AF_INET specifys that IPv4 is being used
# SOCK_STREAM specifys that this is a TCP socket 
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The client connects to a server that is actively listening for connctions
client_sock.connect((host, port))

# The client application gets input data from the user and 
# sends it to the server
while True:
    # data is received and printed to the user (including welcome banner)
    data = client_sock.recv(1024).decode('utf-8')
    print(data)

    # Data is obtained from user input
    dataToSend = input()

    # if the user wants to exit, the exit code is sent to the server
    # the good bye banner is received and printed
    # finally the connection is closed and the code exits
    if dataToSend == '1 / 0':
        client_sock.send('1 / 0\r\n'.encode('utf-8'))
        goodbyeMessage = client_sock.recv(1024).decode('utf-8')
        print(goodbyeMessage)
        client_sock.close()
        break

    # if the data sent is not 'exit' the data is sent to the server
    # '\r\n' is appended to the string and sent
    dataToSend = dataToSend + '\r\n'
    client_sock.send(dataToSend.encode('utf-8'))