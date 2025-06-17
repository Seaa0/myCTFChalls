#!sage
from Crypto.Util.number import bytes_to_long, getPrime
from random import randint, getrandbits

flag = 'ictf{test_flag}'
m = bytes_to_long(flag.encode())

p = getPrime(550)
q = getPrime(512)
r = getPrime(512)
priv = [getrandbits(512),getrandbits(512)]
n = p*q*r
e = 65537
c = pow(m,e,n)

P.<x> = PolynomialRing(ZZ)
x = P.gen()

def genPoly(p,degree,replace = False,replaceIndex = None, replaceValue = None):
    if replace and (replaceIndex == None or replaceValue == None):
        return False
    terms = [x**i for i in range(degree)]
    coeffs = [13371337]+[randint(1,isqrt(p)) for _ in range(degree-1)]
    if replace:
        coeffs[replaceIndex] = replaceValue
    f = sum([coeff*term for coeff,term in zip(coeffs,terms)])
    return f

f0 = genPoly(p,13,True,1,q)
f1 = genPoly(p,13,True,1,r)

f2, f3, f4 = [genPoly(p,13) for _ in range(3)]
assert gcd(f2,gcd(f3,f4)) == 1

f2 *= (f1*f0)
f3 *= (f1*f0)
f4 *= (f1*f0)

pub = []
for i in range(2,5):
    pub.append(eval('pow(priv[0],priv[1],f'+str(i)+'(p))'))

with open('out.txt','w') as file:
    file.write(f'{n = }\n')
    file.write(f'{e = }\n')
    file.write(f'{c = }\n')
    file.write(f'{p = }\n')
    file.write(f'{pub = }')