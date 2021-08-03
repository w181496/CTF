### gpushop

This challenge gives a package of very complicated source code.

Inside are the haproxy, varnish, and two laravel websites(nginx+php-fpm).

I spent a lot of time looking at the architecture at the beginning. Simply put, haproxy will forward the request to the backend gpushop and paymeflare.

The concept of paymeflare is a bit like cloudflare (the name is also very similar), you can add a domain and bind it with `ip:port` (`CNAME` need to point to the challenge domain)

gpushop is a shopping website (ETH payment). What's more special is that it judges whether the purchase is successful depends on whether the wallet address in the `X-Wallet` header has enough ETH.

And `X-Wallet` header is added by haproxy. By default, it will randomly generate an address for you.

As long as the path is `/checkout`, haproxy will add `X-Wallet` header for you.

```=
acl is_checkout path_dir checkout
http-request lua.gen_addr if is_checkout
http-request set-header X-Wallet %[var(txn.wallet)] if is_checkout
```

So the goal is obviously to find a way to get rid of this header.

<br>

According to experience, this multi-layer architecture is usually prone to problems with url path parsing.

So my first instinct was to try `/checkouT` first and bring my own `X-Wallet` header, but it failed.

Next, I tried `/checkou%74`, then it succeeded!

```=
POST /cart/checkou%74 HTTP/1.1
Host: gpushop.2021.ctfcompetition.com
x-wallet: 0000000000000000000000000000000000000000
```

After sending this request, the `x-wallet` was successfully be overwritten, and then I got the flag...WTF

![](https://github.com/w181496/CTF/blob/master/googlectf-2021-qual/gpushop/gpushop.png?raw=true)

`CTF{fdc990bd13fa3a0e760a14b560dd658c}`
