import socket
import pickle

from poc import MiniKyber, Kyber, Nose, Skipper2Negated, Skipper4, BinomialDistribution
from sage.crypto.mq.rijndael_gf import RijndaelGF

#AES Block size 128, key length 256
rgf = RijndaelGF(4, 6)

#Init sockets
clientSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSideSocket.bind((socket.gethostname(), 8090))
clientSideSocket.listen(5)
clientsocket, address = clientSideSocket.accept()
print("Connection has been established")

HEADERSIZE = 10


try:
    while True:
        serverproxyPK = ()
        msg = clientsocket.recv(1024)
        print("Message has been received")
        y = 65536
        #Connect with serverproxy 
        serverproxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverproxySocket.connect(("stempoljos.westeurope.cloudapp.azure.com", 8092))

        #Wait for PK from server
        pqDataStream = serverproxySocket.recv(y)
        serverproxyPK = pickle.loads(pqDataStream)
        #serverproxyPK = serverproxyPK.decode("utf-8")
        print(serverproxyPK)

        #Generate AES key
        aesKey = "000102030405060708090a0b0c0d0e0f1011121314151617"

        #Generate Post Quantum Keys
        clientproxyPublickey, clientproxyPrivatekey = Kyber.key_gen()

        #Encrypt AES with Post Quantum PK from server and send to serverproxy
        encryptedAesKey = Kyber.enc(serverproxyPK, m=aesKey)
        serverproxySocket.send(bytes(encryptedAesKey))

        #send message to serverproxy with AES
        aesEncryptedMsg = rgf.encrypt(msg, aesKey)
        serverproxySocket.send(bytes(aesEncryptedMsg))

        #listen for response and decrypt with AES key
        response = serverproxySocket.recv(1024)
        response = rgf.decrypt(response, aesKey)
        clientsocket.send(bytes(response))


        serverproxySocket.close()
except socket.timeout:
    clientsocket.close()
    clientSideSocket.close()


