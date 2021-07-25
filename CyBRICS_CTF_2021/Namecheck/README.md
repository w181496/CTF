# Namecheck

這題蠻好玩的

OSINT題

題目給 .bashrc, .bash_history, .profile 和 .ssh/key

要你找本人的名字

其中 .bash_history:

```
git add *
git commit -m "instagram filter"
git push origin main
rm *
ls -la
rm -rf .git
```

所以猜測跟git有關

直接用ssh key踹github登入:

```
$ ssh -i .ssh/key git@github.com
The authenticity of host 'github.com (13.114.40.48)' can't be established.
RSA key fingerprint is SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'github.com,13.114.40.48' (RSA) to the list of known hosts.
PTY allocation request failed on channel 0

Hi poggersdog12! You've successfully authenticated, but GitHub does not provide shell access.
Connection to github.com closed.
```

可以知道使用者名: `poggersdog12`

<br>

ssh-add時會噴`Identity added: .ssh/key (vividcoala@localhost)`

接著開始用這些資訊肉搜

會找到 https://www.instagram.com/vividcoala/

其中該使用者限時動態:

![](https://github.com/w181496/CTF/blob/master/CyBRICS_CTF_2021/Namecheck/ig.png)

掃一下機票的barcode會得到:

```
M1DIVOV/NIKOLAI MR EQCMYKK SVOLEDSU 0024 197Y020D0053 162<532
1MR1197BSU                                        2A555604939055
9 1                          N
```

flag: `DIVOV NIKOLAI`



