# Product Manager

We're given the php source code: `add.php`, `db.php`, `footer.php`, `header.php`, `index.php`,  `view.php`.

And there are some simple MySQL instructions in it, but all sql statements prepared well.

In the `db.php`, it shows us the table structure:

```sql
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
```

We should login as `facebook` to get the flag in the database.

But we can't SQL Injection and we don't have the password of the user `facebook`.

Since that data type of `name` column in the table `products` is `char(64)`, so maybe we can try MySQL Truncation vulnerability to insert a different `facebook` user.

In non-strict mode, if we insert a very long value to `varchar` or `char`, it will cause the result to be truncated.

(In August 2008, Stefan Esser put forward the SQL column truncation attack)

Exploit:

1. Register (Note: the `_` is ` `(Space))
    - username: ```facebook________________________________________________________kaibro```
    - password: `ka1bro8!gGG`
2. It will truncate the username and then store the username `facebook` with password `ka1bro8!gGG` into database.

3. Login with username `facebook` and password `ka1bro8!gGG` at `view.php`
4. get the flag!

![](https://github.com/w181496/CTF/raw/master/fbctf2019/ProductsManager/pm.png)

flag: `fb{4774ck1n9_5q1_w17h0u7_1nj3c710n_15_4m421n9_:)}`

