import socket

from poc import MiniKyber, Kyber, Nose, Skipper2Negated, Skipper4, BinomialDistribution
from sage.crypto.mq.rijndael_gf import RijndaelGF

rgf = RijndaelGF(4, 6)


#Init sockets
serverproxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverproxySocket.bind((socket.gethostname(), 8092))
serverproxySocket.listen(5)

serversideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversideSocket.connect((socket.gethostname(), 8094))

while True:
    #Establish connection with clientproxy
    clientproxySocket, address = serverproxySocket.accept()
    print("Tunnel has been established")

    #Generate Post Quantum Keypair
    serverproxyPublickey, serverproxyPrivatekey = Kyber.key_gen()
    #print (serverproxyPublickey)

    #Send Post Quantum Public key to clientproxy
    clientproxySocket.send(bytes(serverproxyPublickey))

    #Wait for Post Quantum encrypted AES key and decrypt
    aesKey = clientproxySocket.recv(1024)
    aesKey = Kyber.dec(serverproxyPrivatekey, c=aesKey)

    #Wait for message encrypted with AES and decrypt   
    msg = clientproxySocket.recv(1024)
    msg = rgf.decrypt(msg, aesKey)

    #send message to serverside
    serversideSocket.send(bytes(msg))

    #wait for response
    response = serversideSocket.recv(1024)

    #Encrypt response with AES key and send to clientproxy
    encryptedresponse = rgf.encrypt(response, aesKey)
    clientproxySocket.send(bytes(encryptedresponse))
    clientproxySocket.close()

    
serverproxySocket.close()
serversideSocket.close()