from pwn import *

rr = remote('140.110.112.29', 5132)

l = 0
r = 90000000000

for i in range(9999):

        rr.recvuntil('>')
        rr.sendline('4')
        rr.recvuntil(' : ')
        mid = (l+r)/2
        rr.sendline(str(mid))
        s = rr.recvline()
        print s
        if "not" in s:
                l = mid + 1
        elif "too" in s:
                r = mid
        else:
                break
