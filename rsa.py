import math
import numpy as np
import sys

def convert(m):
    global alphabet
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    global cypher
    cypher = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    converted = []
    for i in m:
        if i in alphabet:
            ind = alphabet.index(i)
            converted.append(cypher[ind])
    return converted


def encrypt(n, d, e, m):
    converted = convert(m)
    encrypted = []
    for i in converted:
        c = i**e % n
        encrypted.append(c)

    return encrypted


def decrypt(n, d, e, m):
    decrypted = []
    for i in m:
        val = i**d % n
        for j, k in zip(cypher, alphabet):
            if val == j:
                decrypted.append(k)
    return decrypted

def gcd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return max(a, b)

def coprime(a, b):
    return gcd(a, b) == 1

def rsa(p, q, m):
    n = p*q
    phi = (p-1)*(q-1)
    print(phi)
    e = 3
    d = 1

    noe = True
    while noe:
        val = coprime(phi, e)
        if val == True:
            print('Found e: ', e)
            break
        else:
            e += 1

    unfound = True
    while unfound:
        if d*e % phi == 1:
            print('Found d: ', d)
            unfound = False
        else:
            d += 2


    encrypted = encrypt(n, d, e, m)
    print('Encrypted: ', encrypted)
    decrypted = ''.join(decrypt(n, d, e, encrypted))
    print('Decrypted: ', decrypted)

p = int(sys.argv[1])
q = int(sys.argv[2])
m = sys.argv[3]

rsa(p, q, m)
