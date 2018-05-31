from pwn import *

rr = remote('140.110.112.29', 5122)

for i in range(101):
        print "Time:",i
        rr.recvuntil("polynomial : ")
        if i == 0:
                continue
        s = rr.recvline()[:-1]
        arr = s.split(' ')
        print arr
        print "len:",len(arr)

        for j in range(99999):
                tmp = 0
                for k in range(len(arr)):
                        tmp += int(arr[len(arr) - 1 - k]) * (j ** k)
                if tmp == 0:
                        print j
                        rr.sendline(str(j))
                        break
                j = -1 * j
                tmp = 0
                for k in range(len(arr)):
                        tmp += int(arr[len(arr) - 1 - k]) * (j ** k)
                if tmp == 0:
                        print j
                        rr.sendline(str(j))
                        break

rr.interactive()
