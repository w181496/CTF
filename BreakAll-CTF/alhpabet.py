from pwn import *

rr = remote('140.110.112.29', 5128)

for i in range(100):
        c = rr.recvuntil(' in ')[-5]
        print c
        s = rr.recvline()
        print s
        ans = 0
        for j in s:
                if j == c:
                        ans+=1
        rr.sendline(str(ans))
rr.interactive()
