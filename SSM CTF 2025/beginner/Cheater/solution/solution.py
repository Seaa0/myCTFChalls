from math import gcd
from Crypto.Util.number import bytes_to_long, long_to_bytes
from gmpy2 import iroot

n = 46884503505861237425470108781013151709608385156407042535162658655219198293531603954762072725496274761369924515589793971505529848123272005525045726561087298432276907310910641955233378153675627867971707733693334181779557896862253210884460657132373758389569573567937002331226015986481271527653964521274862740761
c = b'\x05dT!$O\xa9\xa7r\xce}l!\xf5:L\xcd\x9eq\xc9\x12\x98\x05\xc6+o\xd5\x06\x8b\xebp\x82\x1fu\xf4\x85O\xf5\xaa\x1c\xed\xc7\x86\xe8\x9dz\xa2=\x90\xe0f\xd7\xbb\x81\x1e\xf9\xab\xe71)\x1b\x994\xdd\xa7F\xc16\xff\x87\xbb/;\xea.U\xd7\x9be\xb7^\xef\x9f\xb1\x8e\xd6:\xb1\xafP\xeb5\xf4\xe5\x94\xd0\x8a\xd9[O\x1d=r\xf9\xaf\xdf-\xc3k\xb9\x95\x90\nZ:\x07"\xa5\' \x80\xc0\'R\x9a\xd5`7/\x89\xbf\x7f$u\x08\xecZw\xa6*\xb2\xe4Frr\xbd\xf5G\xf9\xcf\x90\x9a\xd6\xb5S\xdc]\xebB\xf7'
e = 65537

p1 = gcd(bytes_to_long(c), n)
p2 = iroot(n // (p1 ** 2), 2)[0]

phi = p1 * (p1 - 1) * p2 * (p2 - 1)
d = pow(e, -1, phi)

m = pow(bytes_to_long(c) // p1, d, n)
print(long_to_bytes(m))