#!sage
from sage.all import EllipticCurve, GF
from secret import r,flag
from Crypto.Util.number import getPrime, isPrime, bytes_to_long
from random import choice

class ECSA:
    def __init__(self, e, b, N):
        assert e % 2 == 0
        self.e = e
        self.b = b
        self.N = N
    def lift_x(self, x):
        yield (pow(x,self.e//2,self.N)+self.b) % self.N
        yield (-(pow(x,self.e//2,self.N)+self.b)) % self.N

p,q,s= [getPrime(256) for _ in range(3)]
assert isPrime(r)


a1 = 59
b1 = 28
a2 = 12013278315538447858528492054659222553764005924268130578980259416759339149784
b2 = 34812348137058347239824726793851394028362678168738873939877638588406041210697

Ep = EllipticCurve(GF(p),[a1,b1])
Eq = EllipticCurve(GF(q),[a1,b1])
Er = EllipticCurve(GF(r),[a2,b2])
Es = EllipticCurve(GF(s),[a2,b2])

assert p != Ep.order()
assert q != Eq.order()
assert s != Es.order()

n = p*q*r*s*2**2048
En = Ep.order()*Eq.order()*Er.order()*Es.order()

first = ECSA(131074,b1,n)
C1 = choice(list(first.lift_x(bytes_to_long(flag))))
C1 = str(C1)
C1l = len(C1)
print('C1l =',C1l)


Gr = Er.gen(0)
print('Gr =',Gr)

Crs = []
for i in range(0,len(C1)+1,70):
    C1sect = int(C1[i:i+70])
    Cr = (C1sect*Gr)
    Crs.append(Cr)
print('Crs =',Crs)

Gs = Es.gen(0)
print('Gs =',Gs)

final = ECSA(6,b2,n)
C0 = choice(list(final.lift_x(En)))

print('C0 =',C0)
print('n =',n)
