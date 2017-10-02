#!/usr/bin/python

import random

KEY = 'musZTXmxV58UdwiKt8Tp'

def xor_str(x, y):
    if len(x) > len(y):
        return ''.join([chr(ord(z) ^ ord(p)) for (z, p) in zip(x[:len(y)], y)])
    else:
        return ''.join([chr(ord(z) ^ ord(p)) for (z, p) in zip(x, y[:len(x)])])

#flag, key = FLAG.encode('hex'), KEY.encode('hex')
#enc = xor_str(key * (len(flag) // len(key) + 1), flag).encode('hex')

key = KEY.encode('hex')
ef = open('flag.enc', 'r')
content = ef.read()
ef.close()

dec = xor_str(key * (len(content) // len(key) + 1), content)



ef2 = open('res.png', 'w')
ef2.write(dec.decode('hex'))
ef2.close()

#ef = open('flag.enc', 'w')
#ef.write(enc.decode('hex'))
#ef.close()
