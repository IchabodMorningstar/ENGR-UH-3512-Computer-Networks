import socket
import base64
import ssl
import time

mail_server = "smtp.gmail.com"
port = 587
sender = "ludwigfornetworks@gmail.com"
receiver = "ys4950@nyu.edu"
password = "yldnwmcodyvfnhzu"
text = "Do You Miss Miss Me"

# TCP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mail_server, port))
recv0 = clientSocket.recv(1024).decode()
print(recv0)
if recv0[:3] != "220":
    print("220 response failed")

# EHLO
helomsg = "EHLO Ludwig\r\n"
clientSocket.send(helomsg.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != "250":
    print("250 response failed")

# TLS
sslmsg = "STARTTLS\r\n"
clientSocket.send(sslmsg.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != "220":
    print("220 response failed")
context = ssl.create_default_context()
sslClientSocket = context.wrap_socket(
    clientSocket, server_hostname='smtp.gmail.com')

# LOGIN
sslmsg = "AUTH LOGIN\r\n"
sslClientSocket.send(sslmsg.encode())
recv3 = sslClientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != "334":
    print("334 response failed")

# Username
username = base64.b64encode(sender.encode()).decode() + '\r\n'
sslClientSocket.send(username.encode())
recv4 = sslClientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != "334":
    print("334 response failed")

# Password
psw = base64.b64encode(password.encode()).decode() + '\r\n'
sslClientSocket.send(psw.encode())
recv5 = sslClientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != "235":
    print("334 response failed")

for i in range(16):
    # From
    mail_from = "MAIL FROM:<{}>\r\n".format(sender)
    sslClientSocket.send(mail_from.encode())
    recv6 = sslClientSocket.recv(1024).decode()
    print(recv6)
    if recv6[:3] != "250":
        print("250 response failed")

    # To
    mail_to = "RCPT TO:<{}>\r\n".format(receiver)
    sslClientSocket.send(mail_to.encode())
    recv7 = sslClientSocket.recv(1024).decode()
    print(recv7)
    if recv7[:3] != "250":
        print("250 response failed")

    # Data
    datamsg = "DATA\r\n"
    sslClientSocket.sendall(datamsg.encode())
    recv8 = sslClientSocket.recv(1024).decode()
    print(recv8)
    if recv8[:3] != "354":
        print("354 response failed")

    # Mail
    msg = "Subject: {sbj}\r\nDate: {date}\r\nFrom: {sender}\r\nTo: {receiver}\r\n{msg}\r\n.\r\n".format(
        sbj=f"Do You Miss Miss Me{'!'*(1+i)}", date=time.time(), sender=sender, receiver=receiver, msg=text)
    sslClientSocket.send(msg.encode())
    recv9 = sslClientSocket.recv(1024).decode()
    print(recv9)
    if recv9[:3] != "250":
        print("250 response failed")

# Quit
quitmsg = "QUIT\r\n"
sslClientSocket.sendall(quitmsg.encode())
recv10 = sslClientSocket.recv(1024).decode()
print(recv10)
if recv10[:3] != "221":
    print("221 response failed")

# Close
sslClientSocket.close()
