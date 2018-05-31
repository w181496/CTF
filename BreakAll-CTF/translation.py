from pwn import *

rr = remote('140.110.112.29', 5123)

for i in range(100):
        rr.recvuntil("by ")
        s = rr.recvuntil(" : ")[:-3]
        print s
        g = rr.recvline()[:-1]
        print g
        ans = ''
        for j in range(len(g)):
                if ord(g[j]) >= 65 and ord(g[j]) <= 90:
                        ans += chr((ord(g[j]) -  65 + int(s)) % 26 + 65)
                else:
                        ans += g[j]
        print ans
        rr.sendline(ans)
rr.interactive()
