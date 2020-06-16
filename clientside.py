import socket
import time

#Init sockets
clientproxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientproxySocket.connect((socket.gethostname(), 8090))

#Enter commandline message here
msg = "curl http://localhost:8086/health"

#Enter amount of times the message should be sent
amount = 1000
totaltimetakenall = 0

for x in range(amount):
    starttime = time.time_ns()
    #Send the message to clientproxy
    clientproxySocket.send(bytes(msg, "utf-8"))
    print("Message was send succesfully")
    #Wait for a response
    response = clientproxySocket.recv(1024)
    #Decode and print the response
    decodedResponse = response.decode("utf-8")
    print(decodedResponse)
    timetaken = time.time_ns()-starttime
    totaltimetakenall += timetaken
    print(timetaken)

print("average time taken: ")
print(totaltimetakenall/amount)

clientproxySocket.close()