import socket
import base64
import ssl
import time

mail_server = "smtp.gmail.com"
port = 587
sender = "ludwigfornetworks@gmail.com"
receiver = "cc7486@nyu.edu"
password = "yldnwmcodyvfnhzu"
text = ""
myfile = open(
    r"C:\Users\Changlan Chen\Desktop\NYUSH\Networks\Lab 5\emailBody.txt", "r")

myline = myfile.readline()
subject = myline[9:].rstrip("\n")
myline = myfile.readline()
while myfile:
    myline = myfile.readline()
    if myline == "":
        break
    if myline[0] == ".":
        myline = "." + myline
    myline = myline.rstrip("\n")
    text += myline + "\r\n"
myfile.close()

# TCP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mail_server, port))
recv0 = clientSocket.recv(1024).decode()
print(recv0)
if recv0[:3] != "220":
    print("220 response failed")

# HELO
helomsg = "HELO Ludwig\r\n"
clientSocket.send(helomsg.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != "250":
    print("250 response failed")

# From
mail_from = "MAIL FROM:<{}>\r\n".format(sender)
clientSocket.send(mail_from.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != "250":
    print("250 response failed")

# To
mail_to = "RCPT TO:<{}>\r\n".format(receiver)
clientSocket.send(mail_to.encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)
if recv7[:3] != "250":
    print("250 response failed")

# Data
datamsg = "DATA\r\n"
clientSocket.sendall(datamsg.encode())
recv8 = clientSocket.recv(1024).decode()
print(recv8)
if recv8[:3] != "354":
    print("354 response failed")

# Mail
msg = "Subject: {sbj}\r\nDate: {date}\r\nFrom: {sender}\r\nTo: {receiver}\r\n{msg}\r\n.\r\n".format(
    sbj=subject, date=time.time(), sender=sender, receiver=receiver, msg=text)
clientSocket.send(msg.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)
if recv9[:3] != "250":
    print("250 response failed")

# Quit
quitmsg = "QUIT\r\n"
clientSocket.sendall(quitmsg.encode())
recv10 = clientSocket.recv(1024).decode()
print(recv10)
if recv10[:3] != "221":
    print("221 response failed")

# Close
clientSocket.close()
