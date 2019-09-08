# N1EGG-A waf, a world

![](https://github.com/w181496/CTF/blob/master/n1ctf2019/n1egg-a_waf_a_world/waf.png)

只隨便檢查幾個關鍵字，就Rank 1到比賽結束了......

script:

```php
<?php

$case = file_get_contents('php://input');
if(strpos($case,'eval(')!==false){
    die('webshell');
} else if(strpos($case, 'system(') !== false) {
    die('webshell');
} else if(strpos($case, 'assert(') !== false) {
    die('webshell');
} else if(strpos($case, 'shell_exec(') !== false) {
    die('webshell');
} else if(strpos($case, 'passthru(') !== false) {
    die('webshell');
} else if(strpos($case, '{${') !== false) {
    die('webshell');
} else if(strpos($case, 'extract(') !== false) {
    die('webshell');
} else if(strpos($case, 'base64_decode(') !== false) {
    die('webshell');
} else if(strpos($case, 'gzuncompress(') !== false) {
    die('webshell');
} else if(strpos($case, 'array_map(') !== false) {
    die('webshell');
} else if(strpos($case, '¾¬¬º­«') !== false) {
    die('webshell');
} else if(strpos($case, 'include($') !== false) {
    die('webshell');
} else if(strpos($case, '`$_POST') !== false) {
    die('webshell');
} else if(strpos($case, '`$_REQUEST') !== false) {
    die('webshell');
} else if(strpos($case, 'preg_replace(') !== false) {
    die('webshell');
} else if(strpos($case, '"."') !== false) {
    die('webshell');
} else if(strpos($case, '"^"') !== false) {
    die('webshell');
} else if(strpos($case, 'shell') !== false) {
    die('webshell');
} else if(strpos($case, ')($') !== false) {
    die('webshell');
} else if(strpos($case, 'mail(') !== false) {
    die('webshell');
} else if(stripos($case, 'ld(') !== false) {
    die('webshell');
} else if(stripos($case, 'link(') !== false) {
    die('webshell');
} else{
    die('no-webshell');
}
```
