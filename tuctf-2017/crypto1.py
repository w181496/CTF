# 寫得很亂=.=
from pwn import *

r = remote('neverending.tuctf.com', 12345)
time = 0
while time < 50:
	text="a 	?.!_/:,&@"
	r.sendline(text)
	r.recvuntil("is ")
	enc = r.recvuntil("\n")
	print "ref enc:", enc
		
	r.recvuntil("is ")
	qq = r.recvuntil(" dec")[:-4]
	print "ans_enc:", qq
	
	off = (ord(enc[0]) - ord('a'))
	print "offset:", off

	ans = ""
	for i in qq:
		tmp = ord(chr(ord(i) - off))
		if tmp < 30:
			tmp = (125 - 30 + (tmp))
		if (tmp >= ord('a') and tmp <= ord('z')) or (tmp >=ord('A') and tmp <= ord('Z')):
			ans += chr(tmp)
		else :
			idx = enc.find(i)
			if idx == -1:
				print "i:",i,idx
			ans += text[idx]
	print ans

	r.sendline(ans)
	time = time + 1
	print " ======= ", time-1, "======="
	if time == 50:
		r.interactive()
	sleep(0.3)
	print r.recvuntil(":")
