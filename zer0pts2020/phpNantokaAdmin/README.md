# phpNantokaAdmin

功能: 

- 會自動建立 random name 的 sqlite db
- 可以建立指定`table_name`的table
- 可以建立指定`column_name`, `type` 的 column
- 可以插入資料到table


其中 `table_name` 和 `type` 可以注入 (沒有被反引號包起來)

```
create table [INJECT] (dummy1 TEXT, dummy2 TEXT, [INJECT])
```

中間會過 `is_valid()` 檢查

能用的特殊字元大概只剩: `!@$%^&_+=|~?<>[]{}:;.`

翻了一下 sqlite 官方文件

https://www.sqlite.org/lang_createtable.html

會發現 CREATE TABLE 後面實際上可以接 SELECT 語法

作用是根據 SELECT 結果去建立一張表格

所以很容易想到可以這樣

`CREATE TABLE a AS SELECT * FROM sqlite_master;`

但這個長度太長 (>32)，而且 `*` 不能使用

所以勢必得用到後面的 `type` 去做繞過

賽中玩到這裡就沒踹了

賽後才知道原來 sqlite 可以這樣玩:

`CREATE TABLE a AS SELECT sql [ (dummy1 TEXT, dummy2 TEXT, ]FROM sqlite_master;`

成功串起 `table_name` 和 `type`

也繞過長度限制

最後 `a` table 裡面就有 flag table name

後面就是用一樣方法去撈 flag
