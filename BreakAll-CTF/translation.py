from pwn import *

rr = remote('140.110.112.29', 5125)

for i in range(101):
        rr.recvuntil("string : ")
        if i == 0:
                continue
        s = rr.recvline()[:-1]
        print s
        ans = 0
        for j in range(len(s)):
                ans += ord(s[len(s) - j - 1]) * (256 ** j)
        print ans
        rr.sendline(str(ans))
rr.interactive()
