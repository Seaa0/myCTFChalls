# Crypto/Change
## Challenge Overview
We are given a pseudo-random number generator (PRNG), and you are tasked to find the earliest occurrence where the `output ^ 1 == the next output`
## Solution
### Finding Seed
Just brute, very brutable range of `32*4`
### Convert the tempers to matrices
For each temper, we generate a matrix such that temper(v) = `V*A`, where V is a vector of the bits of v in GF(2). We do this by collecting the outputs of specially selected inputs to the tempers. Each specially selected input consists of 1 '1' bit and everything else are '0' bits. We iterate through all possible indices of the '1' bit. Each index corresponds to each row in the matrix.
### Deriving the targets
We construct a matrix just like the tempers, but this time using xor 1 as the operating. You could probably generate it manually with an understanding of linear algebra, but we can just take the easy way out and use the same method as above. The target values are values that lie in the left kernel of T-X, where T is each of the temper matrices and X is the xor matrix.
### Finding i
Since we have the seed and i, we can generate a matrix that represents a full cycle of the PRNG. Just multiply the matrices.

Next since the value of `i = k*32+j` where j < 32, we can get possible desired vectors for each value of j. Let’s call these vectors t_i. We are trying to solve a problem similar to matrix dlog, where x*C**(k//32)=t_i. We have x, which is the initial value i.e. 0xdeadbeef00c0ffee, C and t_i. Then we solve the dlog by lifting C to a splitting field, then deriving its Jordan normal form. From there, we assume every Jordan block is 1x1 for ease. The problem is now a dlog of the eigenvalues over a splitting field. We find the order of the eigenvalue generator by factoring the field order, and use Lagrange’s Theorem to confirm the order (this is one of the ways elliptic curve orders are calculated). I used factordb to factor because 2^n-1, which is the order of the splitting field, is very likely to be already factored.