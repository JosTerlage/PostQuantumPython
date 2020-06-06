import functools

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return functools.reduce(lambda a,b : str(a) + str(b), result)

def frombits(bits):
    chars = [int(char) for char in bits]
    for b in range(int(len(chars) / 8)):
        byte = chars[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join([str(char) for char in chars])


aesKey = "000102030405060708090a0b0c0d0e0f1011121314151617"


bits = tobits(aesKey)
print(bits)

key = frombits(bits)
print(type(key))

#print(tobits(aesKey))
#str(tobits(aesKey)).strip('[, ]')