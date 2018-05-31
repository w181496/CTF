from pwn import *
import random

r = remote('140.110.112.29', 5129)

for i in range(101):
        r.recvuntil("L = ")
        l = int(r.recvline()[:-1])
        if i == 0:
                continue
        ok = False
        while ok == False:
                num = 0
                s = 0
                for j in range(l):
                        tmp = random.randint(1, 9)
                        num = num * 10 + tmp
                        s += tmp
                if num % s == 0:
                        ok = True
        r.sendline(str(num))
        print num
r.interactive()
