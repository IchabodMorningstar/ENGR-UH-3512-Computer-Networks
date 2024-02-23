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
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# first the server binds to a specific address and port numer
sock.bind((host, port))

# The server then begins to listen for incoming connections
# This is a system blocking call which means the code will hang
# here until a connection is received
sock.listen(1)

# Once a connection is received, two obects are returned:
#   - conn: object used to communicate with the client
#   - addr: information about the client's IP and source port
conn, addr = sock.accept()

print('connected to IP:', addr[0], 'on port', addr[1])

welcomeBanner = 'Hello! Thanks for connecting to my simple server\n\
To terminate the connection send the operation \'1 / 0\'\n'

# When sending data, this must be encoded
conn.send(welcomeBanner.encode('utf-8'))

# This simple echo server receives data and sends it back to the client
while True:
    # using the .recv() function, data is obtained from the socket
    # the data is then decoded back into a string
    data = conn.recv(1024).decode('utf-8')

    # if "exit" is received, connection is closed and code exits
    if (data == '1 / 0\r\n'):
        closing_message = 'Thanks again for connecting! Bye!\n'
        conn.send(closing_message.encode('utf-8'))
        conn.close()
        break

    # if the data isn't 'exit', the data is echoed back to the user
    data = data.strip('\r\n')
    datalst = data.split()
    if datalst[1] == "+":
        data = data + " = " + str(int(datalst[0]) + int(datalst[2]))
    elif datalst[1] == "-":
        data = data + " = " + str(int(datalst[0]) - int(datalst[2]))
    elif datalst[1] == "*":
        data = data + " = " + str(int(datalst[0]) * int(datalst[2]))
    elif datalst[1] == "/":
        try:
            data = data + " = " + str(int(int(datalst[0]) / int(datalst[2])))
        except ZeroDivisionError:
            data = "ZeroDivisionError"
    elif datalst[1] == "%":
        data = data + " = " + str(int(datalst[0]) % int(datalst[2]))
    elif datalst[1] == "^":
        data = data + " = " + str(int(datalst[0]) ** int(datalst[2]))

    print('received the following data: ' + data)
    message = 'You send the following data: ' + data
    conn.send(message.encode('utf-8'))
