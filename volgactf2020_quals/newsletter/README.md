# newsletter

這題直接給 Source code

後端是 Symfony 套 Twig 模板

可以看到 email 的部分直接可以 SSTI

但是會先過 `filter_var($request->request->get('email', ''), FILTER_VALIDATE_EMAIL)`

所以直覺上沒辦法使用 `()` 等字元，因為 filter_var 不給過

但實際上可以用 `"()"@gmail.com` 這種方式繞過

<br>

原本以為這樣直接套現成 RCE Paylaod 就搞定，結果踹老半天都失敗

後來用 `{{constant('Twig\\Environment::VERSION')}}` 才發現版本是 `3.0.3`

網路上那些招都不適用這個版本

所以代表要找一條新的 Path 去 RCE 或讀檔

踹了各種方向，有發現 Symfony 會額外給 Twig 綁上一些全域變數和函數、Filter 等內容

賽中直覺這邊很有機會，但簡單踹一波沒踹出東西

賽後才發現，居然剛好漏掉一個 function 沒踹到

`'/etc/passwd'|file_excerpt(30)`

這樣就能直接讀檔了

<br>

賽後討論時才知道，這題還有很多解法

例如 twig 原生很多 Filter 可以直接 RCE / 讀檔

e.g. `{{['id']|map('passthru')}}`

(p.s. 然後這題把 flag 放在 passwd，感覺原本預設解法是要我們用讀檔解)
