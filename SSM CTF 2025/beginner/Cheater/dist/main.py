from secret import flag
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

m = bytes_to_long(flag)
e = 65537

n1 = 0
p1 = getPrime(256)
for i in range(1, p1*2, 2):
    n1 += i

n2 = 0
p2 = getPrime(256)
for i in range(1, p2*2, 2):
    n2 += i

n = n1 * n2
print("n =", str(n))

c = pow(m, e, n)

print("c =", str(long_to_bytes(p1 * c)))


# n = 46884503505861237425470108781013151709608385156407042535162658655219198293531603954762072725496274761369924515589793971505529848123272005525045726561087298432276907310910641955233378153675627867971707733693334181779557896862253210884460657132373758389569573567937002331226015986481271527653964521274862740761
# c = b'\x05dT!$O\xa9\xa7r\xce}l!\xf5:L\xcd\x9eq\xc9\x12\x98\x05\xc6+o\xd5\x06\x8b\xebp\x82\x1fu\xf4\x85O\xf5\xaa\x1c\xed\xc7\x86\xe8\x9dz\xa2=\x90\xe0f\xd7\xbb\x81\x1e\xf9\xab\xe71)\x1b\x994\xdd\xa7F\xc16\xff\x87\xbb/;\xea.U\xd7\x9be\xb7^\xef\x9f\xb1\x8e\xd6:\xb1\xafP\xeb5\xf4\xe5\x94\xd0\x8a\xd9[O\x1d=r\xf9\xaf\xdf-\xc3k\xb9\x95\x90\nZ:\x07"\xa5\' \x80\xc0\'R\x9a\xd5`7/\x89\xbf\x7f$u\x08\xecZw\xa6*\xb2\xe4Frr\xbd\xf5G\xf9\xcf\x90\x9a\xd6\xb5S\xdc]\xebB\xf7'