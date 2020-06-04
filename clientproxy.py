import socket

clientSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSideSocket.bind((socket.gethostname(), 8090))
clientSideSocket.listen(5)

clientsocket, address = clientSideSocket.accept()
print("connection has been established")

while True:
    msg = clientsocket.recv(1024)

    #send message to serverproxy
    serverproxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverproxySocket.connect((socket.gethostname(), 8092))
    serverproxySocket.send(bytes(msg))

    #listen for response
    response = serverproxySocket.recv(1024)
    clientsocket.send(bytes(response))


    serverproxySocket.close()

clientsocket.close()
clientSideSocket.close()


