import ssl
import socket

# let's say we have a socket already established
mailserver = 'smtp.gmail.com'
mailPort = 587

# we do some work here to move things along
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver, mailPort))
recv = clientSocket.recv(1024).decode()

# YOUR CODE GOES HERE
# MORE CODE HERE
# To establish the TLS connection we do the following:

context = ssl.create_default_context()
sslClientSocket = context.wrap_socket(clientSocket, server_hostname='smtp.gmail.com')

# Now, to send and receive TLS-encrypted data you should use "sslClientSocket" instead of "clientSocket"

# THE REST OF YOUR CODE GOES HERE