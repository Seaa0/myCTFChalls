from Crypto.Util.number import long_to_bytes
from math import gcd, isqrt
import sys
sys.set_int_max_str_digits(10000)

with open('out.txt','r') as file:
    exec(file.read())

k = gcd(pub[1]-pub[2],pub[2]-pub[0],pub[0]-pub[1])

for i in range(1,1000):
    if k % i == 0:
        fout = k // i
        qPlusr = ((fout % (p**2)) - 13371337*13371337)//(p*13371337)
        # q + r = qPlusr
        # qr = n//p
        # q = qPlusr-r
        # r(qPlusr-r) = n//p
        # -r**2+qPlusr*r-n//p = 0
        # r = (-qPlusr+-sqrt(qPlusr**2-4*-1*-n//p))/2*-1
        if qPlusr**2-4*n//p < 0: # discriminant < 0
            continue
        r = (-qPlusr+isqrt(qPlusr**2-4*n//p))//-2
        if n % r != 0: # try other root
            r = (-qPlusr-isqrt(qPlusr**2-4*n//p))//-2
        if n % r != 0: # value of i is wrong
            continue
        q = n//p//r
        phi = (p-1)*(q-1)*(r-1)
        d = pow(e,-1,phi)
        m = pow(c,d,n)
        print(long_to_bytes(m).decode())
        break