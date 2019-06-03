# rceservice

這題題目很短，用`preg_match`擋了一堆東西

但我們知道PHP有pcre backtrace limit限制，當回溯超過1000000次時，會回傳false

在弱比較下等同匹配成功，就成功繞過惹

payload詳見exp.py
