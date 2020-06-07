# from poc import MiniKyber, Kyber, Nose, Skipper2Negated, Skipper4, BinomialDistribution
# from sage.crypto.mq.rijndael_gf import RijndaelGF

from Crypto.Cipher import AES

#rgf = RijndaelGF(8, 6)

msg = "curl http://localhost:8086/health"
aesKey = "000102030405060708090a0b0c0d0e0f1011121314151617"


def tohex(msg):
    return ''.join(hex(ord(x))[2:] for x in msg)

def fromhex(hexstring):
    return bytearray.fromhex(hexstring).decode()

cipher = AES.new(aesKey, AES.MODE_EAX)

nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(data)

print(cipher)


















# aesEncryptedMsg = rgf.encrypt(tohex(msg), aesKey)
# print(aesEncryptedMsg)

# aesDecryptedMsg = rgf.decrypt(aesEncryptedMsg, aesKey)

# print(fromhex(aesDecryptedMsg))
