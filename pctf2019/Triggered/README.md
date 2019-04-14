# Triggered

## 題目

- 給了一個plpgsql跑的microservice
- plpgsql不是一般的SQL，是postgresql搞出的一個語言
- 找一下可以發現source code: http://triggered.pwni.ng:52856/static/schema.sql
- 我們的Request/Respons和header等的處理都會先經過plpgsql才進到資料庫

## 漏洞

- 1. `POST /login`會設一個uuid到session，並綁上參數`username`指定的user
- 2. `POST /login/password`會去從session抓uuid對應的user密碼來和我們輸入的`password`比對
- 3. 密碼比對相同後，會根據uuid去UPDATE `logged_in=TRUE`

這邊存在一個Race condition漏洞

只要在2.和3.之間去另外跑1.

就能把通過密碼驗證裡session的user改成任意user

做到任意user登入

## FLAG

登入成admin後，搜一下就能找到flag

`PCTF{i_rAt3_p0sTgRE5_1O_oUT_0f_14_pH_n3ed5_m0Re_4Cid}`
