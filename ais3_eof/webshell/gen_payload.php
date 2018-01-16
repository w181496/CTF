<?php
$cmd = $_GET['c'];
$s =  hash('SHA512',$_SERVER['REMOTE_ADDR']) ^ $cmd;
$key = $_SERVER['HTTP_USER_AGENT'] . sha1("webshell.eof-ctf.ais3.ntu.st");
$sig = hash_hmac('SHA512', $cmd, $key);

echo "input sig: ".$sig;
echo "<br>";
echo "input cmd: ".urlencode($s);
