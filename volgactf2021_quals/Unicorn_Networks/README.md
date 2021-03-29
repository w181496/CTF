# Unicorn Networks

查看 HTML src 可以看到這個 API endpoint:

`http://192.46.237.106:3000/api/getUrl?url=http://kaibro.tw:5278`

會收到 Request:

```
GET / HTTP/1.1
Accept: application/json, text/plain, */*
User-Agent: axios/0.21.0
Host: kaibro.tw:5278
Via: 1.1 9a3403815e7c (squid/3.5.27)
X-Forwarded-For: 172.18.0.2
Cache-Control: max-age=259200
Connection: keep-alive
```

可以看到背後有過 squid

然後測一下可以發現 `gopher` 能用

但這些都不太重要XD

<Br>

用 302 redirect 繞過一些本機檢查後，會發現 `127.0.0.1/admin/` 這裡有兩個額外的 API endpoint 可以用

其中一個 `http://127.0.0.1/api/admin/service_info?name=`

`name` 輸入完，會列出一堆 pid, pcpu, pmem 之類的資訊:

```
{"status":"ok","content":[{"name":"bootmisc.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"checkfs.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"checkroot-bootclean.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"checkroot.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"hostname.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"killprocs","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"mountall-bootclean.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"mountall.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"mountdevsubfs.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"mountkernfs.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"mountnfs-bootclean.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"mountnfs.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"nginx","running":true,"startmode":"","pids":[21,23,24],"pcpu":0.9535479917786487,"pmem":0.2},{"name":"procps","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"rc.local","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"sendsigs","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"umountfs","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"umountnfs.sh","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"umountroot","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0},{"name":"urandom","running":false,"startmode":"","pids":[],"pcpu":0,"pmem":0}]}
```

Recon 一下，會發現這個是用到一套叫 `systeminformation` 的 Library: https://github.com/sebhildebrandt/systeminformation

然後不久前出過一個 Command Injection 的洞: https://github.com/ForbiddenProgrammer/CVE-2021-21315-PoC

裡面用 `name[]` 來 bypass 檢查

實際踹了一下，的確用 `name[]=$(cmd)` 就能 shell 惹

`VolgaCTF{ExpRe$$_node_vulns_3719947192}`
