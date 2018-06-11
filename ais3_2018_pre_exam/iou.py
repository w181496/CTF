# AIS3{D0cT0R StRaNG3 - F0rgERy ATTaCk Ag4InsT RSa DIgital SigNatUrE}
from Crypto.Util.number import long_to_bytes
from pwn import *

while True:

    r = remote('104.199.235.135',20002)

    r.recvuntil("x[:6] == '")
    zz = r.recvuntil("'")[:-1]
    print zz
    qq = '000000'
    print qq
    ok = 0
    for i in range(8234560):
        m = hashlib.sha256()
        m.update(zz+str(i))
        #print str(i)+gg
        s = m.hexdigest()
        #print s[:6]
        if s[:6] == qq:
            print zz+str(i), s
            r.sendline(zz + str(i))
            ok = 1
            break

    if ok:
        print "ok"
    else:
        r.close()
        continue
#r.interactive()
    r.recvuntil('n = ')
    n = int(r.recvline()[:-1])

    print("n:", n)

    e = 65537

    num = 100

    gotit = 0

    while True:
            if num > 5000000:
                break
            #tmp = (num ** e) % n
            tmp = pow(num, e, n)
            gg = long_to_bytes(tmp)
            if num % 10 == 0:
                    print("now:",num)
            arr = gg.split()
            if len(arr) > 3:
                ele = arr[3]
                fl = 0
                for i in ele:
                    if i not in ['1','2','3','4','5','6','7','8','9','0', ' ']:
                        fl = 1
                        break
                if fl == 0:
                    bucks = int(arr[3])
                    print bucks
                    if bucks > 10:
                            print("m:",tmp)
                            print("sig:",str(num))
                            print(gg)
                            r.sendline(str(tmp))
                            r.sendline(str(num))
                            print("Found! ",num)
                            gotit = 1
                            break
            num += 1

    if gotit == 1:
        r.interactive()
