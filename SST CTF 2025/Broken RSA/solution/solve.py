from Crypto.Util.number import getPrime, long_to_bytes, isPrime
from math import isqrt
from pwn import *

io = remote('hopper.proxy.rlwy.net',12780)
io.recvline()
e = int(io.recvline().decode().split('exponent: ')[1])

while True:
    p = getPrime(512)
    N = 2*p+1
    if isPrime(N):
        break
io.recvline()
io.sendline(str(N).encode())
io.recvline()
ct = io.recvline().decode().split('go: ')[1]

phi = N-1
d = pow(e,-1,phi//2)
m = pow(ct,d,N)
print(long_to_bytes(m))