# 1linephp

題目基本上只比orange原題多在，會把所有你要引入的檔案路徑加上`.php`後綴

然後另外給你phpinfo資訊(他存成html，不是真的跑phpinfo，所以無法撞)

<br>

比對 phpinfo 跟乾淨 Docker 環境，會發現他有裝 zip

所以方向可能就是往`zip://xxxxxxxx#shell.php`，去繞過後綴限制

而要用zip protocol，勢必得先上傳zip檔

已知的上傳方法就是跟原題一樣用 session upload progress

但是 upload progress 上傳的檔案，會在開頭加上 `upload_progress_`，檔案尾巴也會加上一坨大便

很明顯一般狀況下，這種檔案不會被正常 zip library 視為合法 zip 檔

因此必須對上傳的檔案做些手腳，讓它能被 php libzip 正常解析

<br>

![](https://github.com/w181496/CTF/blob/master/0ctf2021_qual/1linephp/zip_struct.png)

仔細閱讀 zip 結構後，可以知道 php libzip 是先去檔案尾端找 End of Centry Directory (EOCD) 區塊

再從裡頭解析 Central Directory 的 offset，去找到 Central Directory 區塊

Central Directory 基本上就是你整個壓縮檔中的檔案目錄，紀錄每個檔案區塊 (Local File Header) 的位置

所以下一步就是從 Central Directory 中找出 local file header 的 offset

Local file header 區塊中，又能透過 file name length 和 extra field length 等資訊去找到真正的 file data

所以總結來說，php libzip 會從尾端解析，然後透過各個區塊的offset，最後指到真正要解壓縮的檔案區塊

而這題的考點也很明顯

由於解析過程是透過offset去找file data，所以就算開頭是一坨拉機，只要offset正確，它還是能正常解壓縮

所以

預期解：把 Central Directory 和 End of Central Directory 中的 offset (相對檔案開頭) 都加上 16，這樣上傳後，開頭加上16 bytes的大便後，一樣能被正常解析

![](https://github.com/w181496/CTF/blob/master/0ctf2021_qual/1linephp/zip-sol.png)

非預期解：直接把 zip 檔開頭 16 bytes 移除再上傳。 why? 因為 16 bytes 的垃圾不會蓋到 file name length 和 extra field length 等欄位，所以解析時一樣能正常算出file data length等內容





