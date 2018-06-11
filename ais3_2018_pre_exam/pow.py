import hashlib
import math

#r = remote('104.199.235.135', 20000)
#r.recvuntil("x[:6] == '")
#gg = r.recvuntil("'")[:-1]
gg = raw_input(':')
print gg

#r.recvuntil("== '")
#qq = r.recvline()[:-2]
qq = '000000'
print qq
for i in range(823456):
    m = hashlib.sha256()
    m.update(gg+str(i))
    #print str(i)+gg
    s = m.hexdigest()
    #print s[:6]
    if s[:6] == qq:
        print gg+str(i), s
        #r.sendline(str(i))
        break
#r.interactive()
