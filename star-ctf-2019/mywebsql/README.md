# MyWebSQL

[English Version](https://balsn.tw/ctf_writeup/20190427-*ctf/#mywebsql)

這題用了MyWebSQL架

搜一下，很容易可以找到3.7版的RCE漏洞:

[https://github.com/eddietcc/CVEnotes/blob/master/MyWebSQL/RCE/readme.md](https://github.com/eddietcc/CVEnotes/blob/master/MyWebSQL/RCE/readme.md)

RCE步驟:

1. Write PHP code to table
2. Execute Backup database function and set filename to `anything.php`
3. You have a webshell now: `/backups/anything.php`

拿到shell後，`/readflag`還要先解一串隨機運算式才能噴flag

這邊我用`mkfifo`去解決這個問題

```
$ mkfifo pipe
$ cat pipe | /readflag |(read l;read l;echo "$(($l))\n" > pipe;cat) 
<dflag ((read l;read l;echo "$(($l))\n" > pipe;cat)
input your answer:
ok! here is your flag!!
`*ctf{h4E9PKLkr6HTO3JcRglVdYaBSA0eDU8y}`
```
