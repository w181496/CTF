from pwn import *

rr = remote('140.110.112.29', 5127)

for i in range(101):
        print i
        rr.recvuntil('Fahrenheit : ')
        if i ==0:
                continue
        s = (int(rr.recvline()[:-1]))
        print s
        rr.recvuntil("Celsius : ")
        rr.sendline(str((s-32)*5)+"/9")


rr.interactive()
