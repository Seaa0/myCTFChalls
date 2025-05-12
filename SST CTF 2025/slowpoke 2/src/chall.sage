#!sage
from secrets import randbits
from Crypto.Util.number import bytes_to_long, getPrime
flag = b'sstctf{int3gr4ti0n_15_continu0u5_bu+_crypt0gr4phy_i5_d1scret3}'

MODULUS = getPrime(256)*getPrime(256)
coefficients = [randbits(512) for _ in range(7)]

state = bytes_to_long(flag)
assert state < MODULUS

var('x, k')
f = 0

for i, coefficient in zip(range(7),coefficients):
    f += coefficient*x**i

integral_result = sum(f.subs(x=k), k, 0, x)

state = (state+int(integral_result(x=1337133713371337133713371337133713371337133713371337133713371337133713371336)-int(integral_result(x=0))))%MODULUS

print('coefficients =',coefficients)
print('modulus =',MODULUS)
print('state =',state)
