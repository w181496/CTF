from pwn import *

r = remote('140.110.112.29', 5124)

r.recvuntil("f0(x) = ")
f0 = r.recvline()[:-1]

r.recvuntil("f1(x) = ")
f1 = r.recvline()[:-1]

r.recvuntil("f2(x) = ")
f2 = r.recvline()[:-1]

r.recvuntil("f3(x) = ")
f3 = r.recvline()[:-1]

r.recvuntil("f4(x) = ")
f4 = r.recvline()[:-1]

for tt in range(101):
        r.recvuntil("function : ")
        n = int(r.recvline()[:-1])
        r.recvuntil("x = ")
        x = int(r.recvline()[:-1])
        if tt == 0:
                continue
        if n == 0:
                func = f0
        elif n == 1:
                func = f1
        elif n == 2:
                func = f2
        elif n == 3:
                func = f3
        elif n == 4:
                func = f4

        tmp = ''
        for i in func:
                if i == 'x':
                        tmp += '*' + str(x)
                elif i == '^':
                        tmp += '**'
                else:
                        tmp += i
        for gg in range(len(tmp)):
                if tmp[gg] == '*' and gg == 0:
                        tmp = '1' + tmp
                elif tmp[gg] == '*' and tmp[gg-1] == ' ':
                        tmp = tmp[:gg-1] + '1' + tmp[gg:]

        print tmp
        res = eval(tmp)

        print res

        r.sendline(str(res))
r.interactive()
