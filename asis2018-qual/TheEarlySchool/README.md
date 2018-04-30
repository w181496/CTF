# The Early School

my script:

```python
#!/usr/bin/python
from Crypto.Util.number import *

def decrypt(msg):
    ans = ''
    for i in range(len(msg) / 3):
        ans += (msg[3 * i] + msg[3 * i + 1])
    if len(msg) % 3 == 2:
        ans += msg[3 * (len(msg) / 3)]    
    return ans

fp = open('FLAG.enc', 'r')
s = fp.read()
gg = bin(bytes_to_long(s))[2:]

for _ in xrange(20):    # flag in round 18 
    gg = decrypt(gg)
    print _, ":", long_to_bytes(int(gg, 2))
```

`ASIS{50_S1mPl3_CryptO__4__warmup____}`
