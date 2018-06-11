with open('flag-encrypted-511ab4a9fd7bb2d216ab5b5afa7fae5742eef94e', 'r') as data:
    flag = data.read()

def xor(X, Y):
    return ([chr(ord(x) ^ ord(y)) for x, y in zip(X, Y)])

for i in range(256):       
    k = ''
    k += chr(ord(flag[0])^ord('A'))
    k += chr(ord(flag[1])^ord('I'))
    k += chr(ord(flag[2])^ord('S'))
    k += chr(ord(flag[3])^ord('3'))
    k += chr(ord(flag[4])^ord('{'))
    k += chr(79)
    k += chr(46)
    k += chr(146)
    k += chr(167)
    k += chr(i)
    res =  chr(ord(k[8])^ord(k[9])) == flag[159]
    if res:
        print i
        break

tmp = k
l = 10
ans = ''
for i in range(16):
    res = ''
    res = xor(flag[i*l:][:l], tmp)
    for h in res:
        ans += h

print ans
