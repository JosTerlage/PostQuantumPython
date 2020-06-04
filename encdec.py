from poc import MiniKyber, Kyber, Nose, Skipper2Negated, Skipper4, BinomialDistribution

#int pk_server

#listen on port 

message = '10101010'

pk_server, sk_server = Kyber.key_gen()


encrypted = Kyber.enc(pk_server, m=message)

print (encrypted)

decrypted = Kyber.dec(sk_server, c=encrypted)

print (decrypted)

#send to port 8086