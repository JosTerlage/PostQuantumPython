import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 8090))

msg = "curl http://stempoljos.westeurope.cloudapp.azure.com:8086/health"


for x in range(20):

    s.send(bytes(msg, "utf-8"))
    response = s.recv(1024)
    decodedResponse = response.decode("utf-8")
    print(decodedResponse)
    #time.sleep(1)

s.close()