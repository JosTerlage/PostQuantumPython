import socket
import pickle

from poc import MiniKyber, Kyber, Nose, Skipper2Negated, Skipper4, BinomialDistribution
from sage.crypto.mq.rijndael_gf import RijndaelGF

rgf = RijndaelGF(4, 6)

#Init sockets
serverproxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverproxySocket.bind((socket.gethostname(), 8092))
serverproxySocket.listen(5)

serversideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversideSocket.connect((socket.gethostname(), 8094))

def frombits(bits):
    chars = [int(char) for char in bits]
    for b in range(int(len(chars) / 8)):
        byte = chars[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join([str(char) for char in chars])

while True:
    #Establish connection with clientproxy
    clientproxySocket, address = serverproxySocket.accept()
    #clientproxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)

    print("Tunnel has been established")

    #Generate Post Quantum Keypair
    serverproxyPublickey, serverproxyPrivatekey = Kyber.key_gen()
    #print (serverproxyPublickey)

    #Send Post Quantum Public key to clientproxy
    pqDataStream = pickle.dumps(serverproxyPublickey)
    clientproxySocket.send(str(len(pqDataStream)).encode("utf8"))
    clientproxySocket.send(pqDataStream)
    #clientproxySocket.send(b'00000001')


    #Wait for Post Quantum encrypted AES key and decrypt
    aesKey = clientproxySocket.recv(1024)
    aesKey = Kyber.dec(serverproxyPrivatekey, c=aesKey)
    aesKey = frombits(aesKey)

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