# Products Manager

題目直接給 source code

裡面用了一堆 sql 操作

但都處理得很好，沒有 sql injection 的問題

其中db.php:

```
/*
CREATE TABLE products (
  name char(64),
  secret char(64),
  description varchar(250)
);

INSERT INTO products VALUES('facebook', sha256(....), 'FLAG_HERE');
INSERT INTO products VALUES('messenger', sha256(....), ....);
INSERT INTO products VALUES('instagram', sha256(....), ....);
INSERT INTO products VALUES('whatsapp', sha256(....), ....);
INSERT INTO products VALUES('oculus-rift', sha256(....), ....);
*/
```

刻意給出表結構

第一個直覺就是踹 mysql truncation vulnerability (like Wordpress CVE-2009-2762)

在 non-strict mode 下，如果塞超過長度的值到 `CHAR` 或 `VARCHAR` 都會導致結果被 Truncation

註冊`admin___________________________________________________________kaibro` 和一組你自己的密碼

(`_` is Space(空格))

然後就能用你設定的這組密碼登入`admin`惹

因為在db裡面他已經因為過長truncate了，admin 帳號就會多一組出來

![](https://github.com/w181496/CTF/blob/master/fbctf2019/ProductsManager/pm.png)

`fb{4774ck1n9_5q1_w17h0u7_1nj3c710n_15_4m421n9_:)}`
