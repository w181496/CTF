# rbSQL

## 漏洞

這題做的事就是pack和unpack存在檔案當資料庫的概念

`umail`傳陣列，他`strlen`會回傳NULL (他只檢查最大長度，沒檢查最小長度)

由於pack時字串是一組一組串在result結尾

parse時依序parse

但是pack會遞迴下去pack，parse不會遞迴下去parse

(parse最多parse兩層ARR)

所以可以構造umail[]，讓裡面的字串元素去蓋後面的lvl和pwd

最後排法大概是這樣子：

`ARR chr(1) STR chr(strlen(umail[0])) chr(32) md5(password) STR chr(strlen(ip)) ip STR chr(1) 2`

他解析時碰到ARR會當作STR，然後把chr(1)當字串長度，再把STR當成字串內容

接著後面就是我們可控的部分惹


## Payload

`uid=kaibro&upw=test&umail[]=%20098f6bcd4621d373cade4e832627b4f6%01%04test%01%012`

帳號kaibro

密碼test

登入後即可看到flag

`FLAG{akaneTsunemoriIsSoCuteDontYouThinkSo?}`
