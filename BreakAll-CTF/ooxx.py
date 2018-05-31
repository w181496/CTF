# ooxx
from pwn import *

r = remote('140.110.112.29', 5126)

def check(arr):
        f = 0
        for i in range(9):
                if arr[i] == 0:
                        f = 1
                        break
        if f == 0:
                return True
        for i in range(3):
                if(arr[i*3] == arr[i*3+1] and arr[i*3] == arr[i*3+2] and arr[i*3]!=0):
                        return True
                if(arr[i] == arr[i+3] and arr[i] == arr[i+6] and arr[i] !=0):
                        return True
        if arr[0] == arr[4] and arr[0] == arr[8] and arr[0] != 0:
                return True
        if arr[2] == arr[4] and arr[2] == arr[6] and arr[2] != 0:
                return True
        return False

ans = ''
for i in range(83):
        print i
        arr = [0] * 16
        cnt = 0
        first = 1
        for j in range(9):
                if check(arr) == True:
                        break
                r.recvuntil("ai move : ")
                ai = int(r.recvline()[:-1])
                if first == 1:
                        ans = str(ai) + ans
                        first = 0
                arr[ai] = 1
                cnt += 1
                if check(arr) == True:
                        break
                r.recvuntil("your move : ")
                rec = 0
                last = 0
                for k in range(9):
                        if arr[k] == 0:
                                arr[k] = 1
                                if check(arr) == True:
                                        r.sendline(str(k))
                                        arr[k] = 2
                                        rec = 1
                                        break
                                arr[k] = 2
                                if check(arr) == True:
                                        r.sendline(str(k))
                                        arr[k] = 2
                                        rec = 1
                                        break
                                last = k
                                arr[k] = 0
                                #print arr
                if rec == 0:
                        arr[last] = 2
                        r.sendline(str(last))
                if check(arr) == True:
                        break
print ans
r.interactive()
