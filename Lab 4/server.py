import socket
import sys

# buidling up the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) == 2:
    port = int(sys.argv[1])
else:
    port = 8080

# bind the server to local address and port numer
sock.bind(('localhost', port))

# The server then begins to listen for incoming connections
sock.listen(5)

# initialize the visited number
n = 0

# start receiveing
while True:
    # client socket
    conn, addr = sock.accept()

    data = conn.recv(1024).decode('utf-8')

    # check what the browser needs to get
    if data.startswith('GET /page2'):
        n += 1
        goingmsg = '<HTML><HEAD><TITLE>HTTP Homework</TITLE></HEAD><BODY><H3><CENTER>HTTP Homework</CENTER></H3>This is page2<P>You can go <A HREF=" / \
            ">back</A> <P><CENTER>This server has been used {} times</CENTER></BODY></HTML>\r\n'.format(n)
    elif data.startswith('GET /page3'):
        n += 1
        goingmsg = '<HTML><HEAD><TITLE>HTTP Homework</TITLE></HEAD><BODY><H3><CENTER>HTTP Homework</CENTER></H3>This is page3<P>You can go <A HREF=" / \
            ">back</A> <P><CENTER>This server has been used {} times</CENTER></BODY></HTML>\r\n'.format(n)
    elif data.startswith('GET / HTTP/1.1'):
        n += 1
        goingmsg = '<HTML><HEAD><TITLE>HTTP Homework</TITLE></HEAD><BODY><H3><CENTER>HTTP Homework</CENTER></H3>This is the main page<P>You can click on <A HREF="/page2">page 2</A> or <A HREF="/page3">or Page 3</A><P><CENTER>This server has been used {} times</CENTER></BODY></HTML>\r\n'.format(
            n)
    else:
        failmsg = "HTTP/1.1 404 Not Found\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>\r\n"
        conn.sendall(failmsg.encode('utf-8'))
        conn.close()
        continue

    goingmsg = "HTTP/1.0 200 OK\r\nServer: cc7486\r\nContent-Length: {}\r\nContent-Type: text/html\r\nConnection: Closed\r\n\r\n".format(
        len(goingmsg)) + goingmsg
    print(goingmsg)
    conn.sendall(goingmsg.encode('utf-8'))
    conn.close()
