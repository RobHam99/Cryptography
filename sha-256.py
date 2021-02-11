import numpy as np

def Ch(x, y, z):
    """
    Choose; x chooses if output is from y or z.
    """
    return (x & y) ^ (~x & z)

def Maj(x, y, z):
    """
    Majority; x, y, z.
    """
    return (x & y) ^ (x & z) ^ (y & z)

def ROTR(x, n, w=32):
    """
    Rotate right.
    """
    return (x >> n) | (x << (w-n))

def SHR(x, n, w=32):
    """
    Shift right.
    """
    return (x >> n)

def sig0(x):
    """
    Lowercase Sigma 0.
    """
    return ROTR(x, 7) ^ ROTR(x, 18) ^ SHR(x, 3)

def sig1(x):
    """
    Lowercase Sigma 1.
    """
    return ROTR(x, 17) ^ ROTR(x, 19) ^ SHR(x, 10)

def sigma0(x):
    """
    Uppercase Sigma 0.
    """
    return ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22)

def sigma1(x):
    """
    Uppercase Sigma 1.
    """
    return ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25)

def padding(message):
    """
    Turns the message into binary, adds the length of the message in binary to
    the end of the string. Then fills in between the message and the length, with
    0's until the length of the entire message is 512 bits.
    """

    m = ''.join(bin(ord(i)) for i in message).replace('b','') + '1'
    length = len(m)
    m += (448 - (length)) * '0'
    l = "{:064b}".format(length-1)
    m += l
    return m

def parsing(message):
    """
    Parses the newly padded message into 16, 32-bit chunks
    """

    m = padding(message)
    M = []
    for i in range(0, len(m), 32):
        M.append(m[i:i+32])
    return M

def hashing(message):
    """
    Moves block to message schedule, performs hashing operations on message schedule. Returns hashed message.
    'abc' should return: 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
    """

    M = parsing(message)
    H = ['6a09e667', 'bb67ae85', '3c6ef372', 'a54ff53a', '510e527f', '9b05688c', '1f83d9ab', '5be0cd19']
    K = ['428a2f98', '71374491', 'b5c0fbcf', 'e9b5dba5', '3956c25b', '59f111f1', '923f82a4', 'ab1c5ed5', 'd807aa98', '12835b01', '243185be', '550c7dc3', '72be5d74', '80deb1fe', '9bdc06a7', 'c19bf174', 'e49b69c1', 'efbe4786', '0fc19dc6', '240ca1cc', '2de92c6f', '4a7484aa', '5cb0a9dc', '76f988da', '983e5152', 'a831c66d', 'b00327c8', 'bf597fc7', 'c6e00bf3', 'd5a79147', '06ca6351', '14292967', '27b70a85', '2e1b2138', '4d2c6dfc', '53380d13', '650a7354', '766a0abb', '81c2c92e', '92722c85', 'a2bfe8a1', 'a81a664b', 'c24b8b70', 'c76c51a3', 'd192e819', 'd6990624', 'f40e3585', '106aa070', '19a4c116', '1e376c08', '2748774c', '34b0bcb5', '391c0cb3', '4ed8aa4a', '5b9cca4f', '682e6ff3', '748f82ee', '78a5636f', '84c87814', '8cc70208', '90befffa', 'a4506ceb', 'bef9a3f7', 'c67178f2']

    W = []
    wt = 0
    for t in range(64):
        if t <= 15:
            W.append(int(M[t], 2))
        else:
            wt = (((sig1(W[t-2]) + W[t-7]) % 2**32 + sig0(W[t-15])) % 2**32 + W[t-16]) % 2**32
            W.append(wt)
    a = H[0]
    b = H[1]
    c = H[2]
    d = H[3]
    e = H[4]
    f = H[5]
    g = H[6]
    h = H[7]

    for t in range(64):
        T1 = (((((int(h, 16) + sigma1(int(e, 16))) % 2**32) + Ch(int(e, 16), int(f, 16), int(g, 16))) % 2**32 + int(K[t], 16)) % 2**32 + W[t]) % 2**32
        T2 = (sigma0(int(a, 16)) + Maj(int(a, 16), int(b, 16), int(c, 16))) % 2**32
        h = g
        g = f
        f = e
        e = hex((int(d, 16) + T1) % 2**32)
        d = c
        c = b
        b = a
        a = hex((T1 + T2) % 2**32)

    H[0] = hex((int(a, 16) + int(H[0], 16)) % 2**32)
    H[1] = hex((int(b, 16) + int(H[1], 16)) % 2**32)
    H[2] = hex((int(c, 16) + int(H[2], 16)) % 2**32)
    H[3] = hex((int(d, 16) + int(H[3], 16)) % 2**32)
    H[4] = hex((int(e, 16) + int(H[4], 16)) % 2**32)
    H[5] = hex((int(f, 16) + int(H[5], 16)) % 2**32)
    H[6] = hex((int(g, 16) + int(H[6], 16)) % 2**32)
    H[7] = hex((int(h, 16) + int(H[7], 16)) % 2**32)


    return ''.join(['{:x}'.format(int(i, 16)) for i in H])

val = hashing('abcde')

print(val)
