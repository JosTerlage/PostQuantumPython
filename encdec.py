import pickle

from poc import MiniKyber, Kyber, Nose, Skipper2Negated, Skipper4, BinomialDistribution

#int pk_server

#listen on port 

message = '10101010'

pk_server, sk_server = Kyber.key_gen()

print(type(pk_server))


# with open('hardCodedPK.txt', 'wb') as file_object:
#     pickle.dump(pk_server, file_object)

# with open('hardCodedSK.txt', 'wb') as file_object:
#     pickle.dump(sk_server, file_object)


with open('/home/client/Desktop/Python code/hardCodedPK.txt', 'rb') as file_object:
    opened = pickle.load(file_object)

print(type(opened))

#encrypted = Kyber.enc(pk_server, m=message)

#print (encrypted)

#decrypted = Kyber.dec(sk_server, c=encrypted)

# dump = pickle.dumps(pk_server)
# unpack = pickle.loads(dump)
# print(type(dump))
# print(len(dump))


#print (decrypted)
#print (pk_server)

#print(type(pk_server))

#send to port 8086