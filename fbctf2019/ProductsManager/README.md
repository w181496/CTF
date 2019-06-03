# Products Manager

題目直接給source code

裡面用了一堆sql操作

但都處理得很好，沒有sql injection的問題

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

第一個直覺就是踹mysql truncate

註冊`admin___________________________________________________________kaibro`

(`_` 是 空格的意思XD)

然後就能用你設定的這組密碼登入`admin`惹

因為在db裡面他已經因為過長truncate了

`fb{4774ck1n9_5q1_w17h0u7_1nj3c710n_15_4m421n9_:)}`
