#!sage
from Crypto.Util.number import long_to_bytes
P.<x> = PolynomialRing(QQ)
x = P.gen()
with open('out.txt','r') as file:
    exec(file.read().replace('^','**'))

def polyGCD(a,b):
    if b == 0:
        return a.monic()
    return polyGCD(b, a % b)

pm1m = [] # stands for pMinus1Mult
f3 = polyGCD(pub[0][0],pub[1][0])
assert f3 % (x-1) == 0

pm1mult = abs(pub[0][1] - pub[1][1])
pMult = pow(2,pm1mult,n)-1 # Pollard's p-1 factorisation
p = gcd(pMult,n)
assert p > 1
q = n // p
phi = (p-1)*(q-1)
d = pow(e,-1,phi)
m = pow(c,d,n)
print(long_to_bytes(m))