# Can you guess it?

題目: 當帶有 `source` 參數時，會去讀 `$_SERVER['PHP_SELF']` 指定的檔案

但中間會有正規表達式檢查和過一次 `basename()`

```php
if (preg_match('/config\.php\/*$/i', $_SERVER['PHP_SELF'])) {
  exit("I don't know what you are thinking, but I won't let you read it :)");
}

highlight_file(basename($_SERVER['PHP_SELF']));
```

這裡第一眼會覺得正規表達式欠繞

但實際上繞不過

所以第二眼就會想看 `basename()`

打開 php-src 翻一下

感覺檢查長度或是處理字串時，碰到特殊字元可能有問題(?

踹了一下就噴 flag 了

`/index.php/config.php/喵`
