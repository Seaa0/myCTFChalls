from secrets import randbits
from Crypto.Util.number import bytes_to_long, getPrime
flag = b'sstctf{REDACTED}'

MODULUS = getPrime(256)*getPrime(256)
coefficients = [randbits(512) for _ in range(137)]

state = bytes_to_long(flag)
assert state < MODULUS

for x in range(1,1337133713371337133713371337133713371337133713371337133713371337133713371337):
    for i in range(7):
        state += coefficients[i]*x**i
        state %= MODULUS

print('coefficients =',coefficients)
print('modulus =',MODULUS)
print('state =',state)
