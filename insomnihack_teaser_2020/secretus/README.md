# secretus

打開是一個沒任何功能的網頁

掃一下目錄，會看到一堆東西:

```
[20:54:08] 301 -  173B  - /css  ->  /css/
[20:54:11] 301 -   39B  - /debug  ->  /home
[20:54:12] 301 -   39B  - /debug/  ->  /home
[20:54:27] 200 -    1KB - /Home
[20:54:27] 200 -    1KB - /home
[20:54:30] 301 -  173B  - /img  ->  /img/
[20:54:36] 301 -  171B  - /js  ->  /js/
[20:54:56] 200 -  518B  - /package.json
[20:55:13] 401 -   27B  - /secret
[20:55:13] 401 -   27B  - /Secret
[20:55:13] 401 -   27B  - /secret/
[20:55:13] 401 -   27B  - /Secret/
[20:55:37] 200 -  178B  - /vendor/autoload.php
[20:55:37] 200 -  147B  - /vendor/composer/autoload_classmap.php
[20:55:37] 200 -  149B  - /vendor/composer/autoload_namespaces.php
[20:55:37] 200 -  399B  - /vendor/composer/autoload_psr4.php
[20:55:37] 200 -    2KB - /vendor/composer/autoload_real.php
[20:55:37] 200 -    1KB - /vendor/composer/autoload_static.php
[20:55:37] 200 -    4KB - /vendor/composer/installed.json
[20:55:37] 200 -    3KB - /vendor/composer/LICENSE
[20:55:38] 200 -   13KB - /vendor/composer/ClassLoader.php
```

`/secret` 沒辦法訪問

通靈一下之後，發現他 [express-authentication](https://www.npmjs.com/package/express-authentication) 套件用的是預設 secret

所以直接送 `Authorization: secret` 就能繞過

而 `/debug` 底下會把 [session-file-store](https://www.npmjs.com/package/session-file-store) 的 session file 檔名都列出來

但我們目前沒有 key，也沒有任何方式能讀檔

繼續通靈一下

會發現他一樣是用預設的 key 去 sign cookie:

`keyboard cat`

所以用這把 key 去 sign `/debug` 底下每個檔案對應的 session

再去訪問 `/secret`，看哪個人的 session 裡面有 flag 就行惹

![](https://github.com/w181496/CTF/blob/master/insomnihack_teaser_2020/secretus/secretus.png)

`INS{BeSureYourSecretIsActuallySecret}`
