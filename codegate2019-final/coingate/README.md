# coingate

- 這題可以發現明顯的LFI
    - `/?p=home`
    - `/?p=php://filter/convert.base64-encode/resource=config`
    - `/?p=php://filter/convert.base64-encode/resource=admin`
- 所以我們可以讀出任意的php source code
- 比較重要的有以下幾個檔案

admin.php:

```php
<?php
#from Crypto.Cipher import AES
#from Crypto import Random
#import base64

#block_size = 16
#pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
#print 'what you need is just to use python aes'

#plain = "flag"
#plain = pad(plain)

#iv = Random.new().read(AES.block_size)
#key = 'coingate'

#cipher = AES.new(key,AES.MODE_CBC, iv)
#encrypted_text = base64.encodestring(cipher.encrypt(iv+plain))

#print encrypted_text
?>
```
(這邊第一版key是`coingate`，後來主辦方重開變`coingatecoingate`)


config.php:

```php
<?php
//	error_reporting(0);
    $host = "coin_db_1";
    $user = "coin";
    $db_schema = "coin";
	$port = 3306;
    $mysql = new mysqli($host, $user, "", $db_schema,$port);
    $mysql->query("SET NAMES utf8");


?>
```

uploadThumb.php:

```php
<?php
    if($_SESSION['is_login'] !==1 ) die("<script>alert('Login please.');history.back();</script>");
    chdir('uploads');
    $allowExt = Array('jpg','jpeg','png','gif');
    $fname = $_FILES['thumb']['name'];
    $fname = array_pop(explode('./',$fname));
    if(file_exists(urldecode($fname))){

        echo "<script>alert('Already uploaded file.\\nPlease change filename.');history.back();</script>";
    }else{
        $ext = strtolower(array_pop(explode('.',$fname)));
        if($_FILES['thumb']['error'] !== 0){
            die("<script>alert('Upload Error!');history.back();</script>");
        }
        if(!in_array($ext, $allowExt)){
            die("<script>alert('Sorry, not allow extension.');history.back();</script>");
        }

        $contents = file_get_contents($_FILES['thumb']['tmp_name']);
        if($ext=="jpg"){
            if(substr($contents,0,4)!="\xFF\xD8\xFF") die("<script>alert('JPG is corrupted.\\nSorry.');history.back();</script>");
        }else if($ext=="jpeg"){
            if(substr($contents,0,4)!="\xFF\xD8\xFF") die("<script>alert('JPEG is corrupted.\\nSorry.');history.back();</script>");
	}else if($ext=="png"){
            if(substr($contents,0,4)!="\x89PNG") die("<script>alert('PNG is corrupted.\\nSorry.');history.back();</script>");
        }else if($ext=="gif"){
            if(substr($contents,0,4)!="GIF8") die("<script>alert('GIF is corrupted.\\nSorry.');history.back();</script>");
        }else{
            die("<script>alert('Something error.\\nSorry.');history.back();</script>");
        }
	@move_uploaded_file($_FILES['thumb']['tmp_name'], $fname);
	$id = $mysql->real_escape_string($_SESSION['id']);
	$sql = "UPDATE users SET thumb='".$mysql->real_escape_string($fname)."' WHERE id='".$id."'";
	$result = $mysql->query($sql);
	if($result===TRUE){
            $_SESSION['avatar'] = $fname;
            echo("<script>alert('Successfully Avatar Change!');history.back();</script>");
        }else{
            echo("<script>alert('Upload failed!');history.back();</script>");
        }
    }
?>
```

lib.php:

```php
<?php
	ini_set('phar.readonly',0);
    class Requests{
        public $url;

        function __construct($url){
            $this->url = $url;
        }
        function __destruct(){
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $this->url);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $output = curl_exec($ch);
            echo '<div class="description">'.$output.'</div>';
        }
    }
?>
```

- 目標還蠻明確的，上傳一張gif去做phar反序列化，然後SSRF偽造MySQL去做query
    - Payload詳見payload.gif
- 從DB中可以撈出`key{J3qBeP1N9q2w0Pja7kh7Mkh51F6dVdzUcW3eIV4pQwCDgiQqx4N9HnJWBKvF1nGBFoza+AZmW0q9/WKLYeSrVw==}`
- 接著再用admin.php裡面給的key去解AES就能拿到flag
    - `FLAG{Lif2_i5_n0t_alw4ys_what_One_lIke}`

