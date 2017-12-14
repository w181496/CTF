# SqlSrf

Reviewing the source code, we found there is a bug on the cookie.

The cookie(readme) will encrypt/decrypt data.

And there is SQLite injection on the login form.

But when we bypass login to the menu.cgi, we found we need to login as admin to use some additional functionality.

So, we can dump the hash password of admin. (Blind Based)

My dumping script is "exp.rb" in the folder.

The hash-password is:

`d2f37e101c0e76bcc90b5634a5510f64`

 

Then, we can fill the hash password into cookie.

And the cookie will decrypt it to plain password!

The password is:

`Yes!Kusomon!!`

 

After login, there is an wget functionality.

Because the problem description, we know that wget can be used to forge smtp to send a mail. (CRLF injection)

The final payload:

`127.0.0.1 %0D%0AHELO sqlsrf.pwn.seccon.jp%0D%0AMAIL FROM%3A %3Ckaibro%40gmail.com%3E%0D%0ARCPT TO%3A %3Croot%40localhost%3E%0D%0ADATA%0D%0ASubject%3A give me flag%0D%0Aggininder%0D%0A.%0D%0AQUIT%0D%0A:25/`

Then, we will recvie a mail containing encrypted flag.

`37208e07f86ba78a7416ecd535fd874a3b98b964005a5503bcaa41a1c9b42a19`

Again, decrypting it by cookie, then getting the plain-flag.

`SECCON{SSRFisMyFriend!}`
