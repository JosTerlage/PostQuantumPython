import socket
import pickle
import functools

from poc import MiniKyber, Kyber, Nose, Skipper2Negated, Skipper4, BinomialDistribution
from sage.crypto.mq.rijndael_gf import RijndaelGF

#AES Block size 128, key length 256
rgf = RijndaelGF(4, 6)
pqPKLength = 138542

#Init sockets
clientSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSideSocket.bind((socket.gethostname(), 8090))
clientSideSocket.listen(5)
clientsocket, address = clientSideSocket.accept()
print("Connection has been established")

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return functools.reduce(lambda a,b : str(a) + str(b), result)

try:
    while True:
        msg = clientsocket.recv(1024)
        print("Message has been received")
        y = 65536
        #Connect with serverproxy 
        serverproxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #serverproxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
        serverproxySocket.connect(("stempoljos.westeurope.cloudapp.azure.com", 8092))



        """
        #Wait for PK from server
        pqDataStream = []

        # length = serverproxySocket.recv(4096)
        # length = int(str(length, "utf8"))
        # print(length)
        # print(type(length))

        while (int(len(pqDataStream))-1)*4096 <= pqPKLength:
            #print(len(pqDataStream)*4096)
            packet = serverproxySocket.recv(4096)
            #print(packet)
            pqDataStream.append(packet)
        
        #pqDataStream = serverproxySocket.recv(y)
        #print(pqDataStream)
        print(b"".join(pqDataStream))
        serverproxyPK = pickle.loads(b"".join(pqDataStream))
        #serverproxyPK = serverproxyPK.decode("utf-8")
        print(serverproxyPK)
        print(type(serverproxyPK))
        
        
        """


        #Hardcoded the PQ Keys because sending them over the line caused too much trouble
        with open('/home/client/Desktop/Python code/hardCodedPK.txt', 'rb') as file_object:
            serverproxyPK = pickle.load(file_object)



        #Generate AES key
        aesKey = "000102030405060708090a0b0c0d0e0f1011121314151617"
        aesKey = tobits(aesKey)
        
        #Generate Post Quantum Keys
        clientproxyPublickey, clientproxyPrivatekey = Kyber.key_gen()

        #Encrypt AES with Post Quantum PK from server and send to serverproxy
        encryptedAesKey = Kyber.enc(serverproxyPK, m=aesKey)
        print(encryptedAesKey)

        pickledAESKey = pickle.dumps(encryptedAesKey)

        print("Pickled AESKey dumped")
        print(type(pickledAESKey))

        print(len(pickledAESKey))
        serverproxySocket.send(pickledAESKey)

        print("Pickled AESKey sent")

        serverproxySocket.send(bytes("EOS", "utf-8"))

        print("EOS sent")




        #send message to serverproxy with AES
        aesEncryptedMsg = rgf.encrypt(msg, aesKey)
        #serverproxySocket.send(bytes(aesEncryptedMsg))

        #listen for response and decrypt with AES key
        response = serverproxySocket.recv(1024)
        response = rgf.decrypt(response, aesKey)
        clientsocket.send(bytes(response))


        serverproxySocket.close()
except socket.timeout:
    clientsocket.close()
    clientSideSocket.close()


