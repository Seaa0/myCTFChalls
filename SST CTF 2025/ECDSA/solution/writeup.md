# EC(D?)SA
## Prerequisites
To understand the whole challenge concept, you should understand what RSA and ECC (Elliptic Curve Cryptography) are. If not, I recommend going to [Cryptohack](cryptohack.org) to learn. On another note, Cryptohack is also good for learning cryptography in general.
## Overview
This challenge consists of 4 different parts. This writeup features the writeups part by part.  
1. Attacking the first layer of RSA
2. Recovering s
3. Recovering r
4. Recovering p and q
5. Recovering the original CT
6. Decrypting RSA
### Attacking the first layer of RSA
$En^3 < n$, meaning RSA is trivial
### Recovering s
Given a point on $Es$ along with the equation of $Es$, by taking LHS of curve equation - RHS of curve equation, we can recover $0 \mod s$ which we can gcd with $n$ to recover $s$.
### Recovering r
```py
assert p != Ep.order()
assert q != Eq.order()
assert s != Es.order()
```    

In the above `assert` statements, along with the challenge description `...the SMARTest of...`, it is hinted that `Er.order() == r`. Hence, we can gcd $En$ with $n$ to recover $r$.
### Recovering p and q
Given `Ep.order()*Eq.order()` and $pq$, it is trivial to find p and q, using the core principle of how ECM factorisation works.    

Order of $E$ over `Zmod(n)` = `lcm(Ep.order(),Eq.order())`. This means that dividing `Ep.order()*Eq.order()` by a small prime factor has a decent likelihood of being a multiple of `Ep.order()` but not `Eq.order()`.    

When that happens, by Lagrange's Theorem, the resulting point will be the point at infinity $O$. Because of how the elliptic curve point addition algorithm works, this causes a `ZeroDivisionError` as it tries to find the modular inverse of $v \mod pq$, where `gcd(v,pq)` $\neq 1$. Hence, by taking gcd of $v$ and $pq$, we can recover p and hence q.

### Recovering the original CT
As we know, $Er$ is an anomalous curve (`order == modulus`). Using Smart's attack, we can solve ECDLP and recover the original CT.

### Decrypting RSA
Since we know prime factorisation of $n$, we can recover the flag.