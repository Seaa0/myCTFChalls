from Crypto.Util.number import bytes_to_long, getPrime
from random import randint
from math import factorial

flag = b'sstctf{REDACTED}'
m = bytes_to_long(flag)

e = factorial(randint(55,65))*getPrime(256)

try:
    pow(e,-1,getPrime(512)-1)
    print('Wait why does this RSA work? Oh well I won\'t let you decide the modulus then!')
    exit()
except ValueError as E:
    print('See, I told you this RSA wouldn\'t work, it generates the following error:',E)
    pass

print('Here is the exponent:',e)
N = int(input('I\'m so sure that you can\'t break this, I let you decide the modulus!\n'))

assert m < e
print('Here you go:',pow(m,e,N))