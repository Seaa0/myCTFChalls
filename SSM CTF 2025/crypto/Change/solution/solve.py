#!sage
from sage.all import *
from collections import Counter
from itertools import product
from factordb.factordb import FactorDB
from Crypto.Util.number import isPrime, long_to_bytes
from hashlib import sha256
from tqdm import trange

def temper1(y):
    for _ in range(5):
        y ^= (y >> 12)
        y ^= (y << 31) & 0x95fa54741af72bd
        y ^= (y << 27) & 0xdf2a12b81bbaaa21
        y ^= (y >> 5)
    return y

def temper2(y):
    for _ in range(5):
        y ^= (y >> 6)
        y ^= (y << 45) & 0x93b619c288a727f2
        y ^= (y << 21) & 0xb4ef30c811f03be3
        y ^= (y >> 4)
    return y

def temper3(y):
    for _ in range(5):
        y ^= (y >> 15)
        y ^= (y << 37) & 0xa9abc7ad872eb501
        y ^= (y << 28) & 0xdad65256c7af43dd
        y ^= (y >> 5)
    return y

def temper4(y):
    for _ in range(5):
        y ^= (y >> 10)
        y ^= (y << 5) & 0xb475d401139b1ae0
        y ^= (y << 8) & 0x79a2d936fe0515c3
        y ^= (y >> 3)
    return y

def recoverSeed(hints, tempers):
    seed = 0
    for i in range(len(hints)-1):
        for j in range(4):
            if tempers[j](hints[i]) == hints[i+1]:
                seed += (j << (i*2))
    return seed

def getdivisors(factors):
    factor_counts = Counter(factors)
    powers_lists = []
    for p, e in factor_counts.items():
        powers_lists.append([p**i for i in range(e+1)])
    all_divisors = []
    for combo in product(*powers_lists):
        divisor = 1
        for val in combo:
            divisor *= val
        all_divisors.append(divisor)
    return all_divisors

def getorder(element,orderFactors):
    possibleOrders = []
    for divisor in getdivisors(orderFactors):
        if element**divisor == 1:
            possibleOrders.append(divisor)
    return min(possibleOrders)

def matdlog(x,y,matr):
    out = []
    ords = []
    s = None
    mat = matr
    F = mat.minpoly().splitting_field("x")
    matLift = Matrix(F, mat)
    J,P = matLift.jordan_form(transformation=True)
    assert P*J*(P**(-1)) == matLift
    x1 = vector(F,x)*P
    y1 = vector(F,y)*P
    i = -1
    while i < 64: # n = 64
        i += 1
        while x1[i] == 0 or y1[i] == 0:
            i += 1
            if i > 63:
                break
        if i > 63:
            break
        if J[i-1,i]:
            continue
        l = J[i,i]
        lpowered = y1[i]/x1[i]
        for num in out:
            if l**num == lpowered:
                s = num
                break
        if s != None:
            if l**s == lpowered:
                s = None
                continue
        if l != lpowered:
            f = FactorDB(2**F.degree()-1)
            f.connect()
            factors = f.get_factor_list()
            assert all([isPrime(x) for x in factors])
            orde = getorder(l,factors)
            curr = discrete_log(lpowered,l)
            out.append(ZZ(curr))
            ords.append(ZZ(orde))
        k = crt(out,ords)
        if x*matr**k == y:
            return k
    return None

def genMat(temper, inputSize):
    mat = Matrix(GF(2),inputSize,inputSize)
    for i in range(inputSize):
        inp = ['0']*inputSize
        inp[i] = '1'
        out = temper(int(''.join(inp),2))
        out = bin(out)[2:].zfill(inputSize)
        out = [int(x) for x in list(out)]
        mat[i,:] = vector(out)
    return mat

def genCyclemat(mats, seed, cycleSize):
    for i in range(cycleSize):
        curr = 0b11 << ((i % cycleSize)*2)
        curr &= seed
        curr >>= ((i % cycleSize)*2)
        if i == 0:
            cycleMat = mats[curr]
        else:
            cycleMat *= mats[curr]
    return cycleMat

def verify(x,k,seed,cycleMat,matrices,tempers):
    assert 2**100 > k > 0
    testY = x*cycleMat**(k//32)
    
    i = -1
    for i in range(k % 32):
        curr = 0b11 << ((i % 32)*2)
        curr &= seed
        curr >>= ((i % 32)*2)
        testY *= matrices[curr]
    i += 1
    curr = 0b11 << ((i % 32)*2)
    curr &= seed
    curr >>= ((i % 32)*2)
    intTestY = int(''.join([str(digit) for digit in list(testY)]),2)
    if tempers[curr](intTestY) == intTestY^1:
        return 1
    else:
        return 0

if __name__ == '__main__':
    # recovering seed
    tempers = [temper1,temper2,temper3,temper4]
    with open('output.txt','r') as f:
        exec(f.readlines()[0])
    hints = [0xdeadbeef00c0ffee]+hints
    seed = recoverSeed(hints,tempers)
    print('recovered seed:',seed)
    
    # constructing matrices
    inputSize = 64
    mats = [genMat(temper, inputSize) for temper in tempers]

    # xor matrix
    xorOp = lambda a: a^1
    xorMat = genMat(xorOp, inputSize)
    
    # generating target vectors
    targets = [list((mat-xorMat).left_kernel().basis()) for mat in mats]
    assert [len(target) <= 2 for target in targets] # ensure can just use basis vectors, no need to perform addition

    # generating cycleMat
    cycleSize = 32
    cycleMat = genCyclemat(mats,seed,cycleSize)

    # generating starting value
    x = bin(0xdeadbeef00c0ffee)[2:].zfill(64)
    x = vector(GF(2),[int(a) for a in x])

    # offsetting up to one less than a full cycle
    possibles = []
    for i in range(32):
        if not i:
            curr = 0b11 << ((i % 32)*2)
            curr &= seed
            curr >>= ((i % 32)*2)
            possibles.append(targets[curr])
            continue
        curr = 0b11 << ((i % 32)*2)
        curr &= seed
        curr >>= ((i % 32)*2)
        possible = targets[curr]
        if len(targets[curr]) != 0:
            for j in range(i-1,-1,-1):
                curr = 0b11 << ((j % 32)*2)
                curr &= seed
                curr >>= ((j % 32)*2)
                possible = [a*(mats[curr] ** (-1)) for a in possible]
            possibles.append(possible)
        else:
            possibles.append([])

    # performing dlog
    print('dlog started!')
    outKs = []
    for i in trange(32):
        possible = possibles[i]
        for target in possible:
            try:
                curr = matdlog(x,target,cycleMat)*32+i
                outKs.append(curr)
            except (ValueError, IndexError):
                pass # no solution

    out = min(outKs)

    # verify
    assert out < 2**100
    assert verify(x,out,seed,cycleMat,mats, tempers)
    flag = "SSMCTF{%s}"%sha256(long_to_bytes(out)).hexdigest()

    print(flag)
    # SSMCTF{78477e47c80b0a17f58343a73d9bf07ea86622ce300c96ae8c2471ec5ad62dc4}
    # 4 min 11 sec