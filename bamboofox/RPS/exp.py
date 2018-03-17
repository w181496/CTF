from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw',22004)

ans = ["rock","paper","scissors"]

current = 0
time.sleep(3)
for i in range(100):
    print ans[current]
    r.sendline(ans[current])
    current = (current+1)%3
r.interactive()
