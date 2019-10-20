# Option-Cmd-U


http://ocu.chal.seccon.jp:10000/index.php?action=source

主要邏輯在這:

```php
<?php
if (isset($_GET['url'])){
    $url = filter_input(INPUT_GET, 'url');
    $parsed_url = parse_url($url);                        
    if($parsed_url["scheme"] !== "http"){
        // only http: should be allowed. 
        echo 'URL should start with http!';
    } else if (gethostbyname(idn_to_ascii($parsed_url["host"], 0, INTL_IDNA_VARIANT_UTS46)) === gethostbyname("nginx")) {
        // local access to nginx from php-fpm should be blocked.
        echo 'Oops, are you a robot or an attacker?';
    } else {
        // file_get_contents needs idn_to_ascii(): https://stackoverflow.com/questions/40663425/
        highlight_string(file_get_contents(idn_to_ascii($url, 0, INTL_IDNA_VARIANT_UTS46),
                       false,
                       stream_context_create(array(
                           'http' => array(
                               'follow_location' => false,
                               'timeout' => 2
                           )
                       ))));
}
}
```

可以知道目標是訪問 http://nginx/flag.php

然後如果你送的url對應的gethostbyname跟nginx一樣的話，就會被當攻擊者

所以只要知道nginx那台的內網ip，就能透過DNS Rebinding繞過

踹了一下，可以發現ip是`172.18.0.3` (訪問http://nginx/flag.php可以噴當前這台的ip)

直接rebinding炸，就能炸出來

=> `SECCON{what_a_easy_bypass_314208thg0n423g}`
