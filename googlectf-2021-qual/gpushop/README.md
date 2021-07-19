# gpushop

題目給出一包超爆幹複雜的source code

裡面是 k8s 包的 haproxy, varnish, 跟兩台 nginx+php-fpm 架的 laravel 網站

一開始花了不少時間看架構，簡單說就是 haproxy 會 forward request 到後端的 gpushop 和 paymeflare

paymeflare 的概念有點像 cloudflare (名字也像一半)，可以新增一個 domain 並綁上 ip:port (cname指到題目domain)

gpushop 則是一個單純的購物網站(eth付款)，比較特別的是，他判斷是否購買成功是看 `X-Wallet` header 中的錢包地址是否有足夠 eth

而 `X-Wallet` 則是 haproxy 幫你加上去的，預設會隨機幫你產一個地址 

只要路徑是 `/checkout`，haproxy 就會幫你加上 `X-Wallet` header

```
  acl is_checkout path_dir checkout
  http-request lua.gen_addr if is_checkout
  http-request set-header X-Wallet %[var(txn.wallet)] if is_checkout
```

所以目標蠻明顯是想辦法搞掉這個 header

<br>

根據經驗，這種多層架構對 url path 解析通常容易出問題

所以我第一個直覺就是先黑箱踹 `/checkouT`，並帶上自己設的`X-Wallet` header，但失敗

接著我就很自然的踹 `/checkou%74`

然後就成功了!

```
POST /cart/checkou%74 HTTP/1.1
Host: gpushop.2021.ctfcompetition.com
x-wallet: 0000000000000000000000000000000000000000
```

成功把 x-wallet 蓋掉，然後就拿到 flag 了.. WTF

![](https://github.com/w181496/CTF/blob/master/googlectf-2021-qual/gpushop/gpushop.png)

`CTF{fdc990bd13fa3a0e760a14b560dd658c}`


(小tip: 測試時可以先 request 自己設的 domain，看 X-wallet header 還在不在)
