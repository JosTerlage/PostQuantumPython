import socket

serverproxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverproxySocket.bind((socket.gethostname(), 8092))
serverproxySocket.listen(5)

serversideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversideSocket.connect((socket.gethostname(), 8094))

while True:
    clientproxySocket, address = serverproxySocket.accept()
    print("Tunnel has been established")
    msg = clientproxySocket.recv(1024)

    #send message to serverside
    serversideSocket.send(bytes(msg))

    #wait for response
    response = serversideSocket.recv(1024)
    clientproxySocket.send(bytes(response))
    clientproxySocket.close()

    
serverproxySocket.close()
serversideSocket.close()