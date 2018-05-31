from pwn import *
from random import randint
import sympy
r = remote('140.110.112.29', 5131)

for i in range(101):
        print "i:",i
        r.recvuntil("L = ")
        l = int(r.recvline()[:-1])
        print "len:", l
        if i == 0:
                continue
        ok = False
        while ok == False:
                p = sympy.randprime(10 ** (l - 1), 10 ** l)
                tmp = p
                s = 0
                while tmp > 0:
                        s += (tmp %10)
                        tmp /= 10
                if sympy.isprime(s):
                        ok = True
                        r.sendline(str(p))
                        print p
r.interactive()
