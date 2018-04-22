# Timemachine Beta

丟ida pro

可以看到他最後會跑出flag

但是中間卡了一堆sleep

於是...

直接LD_PRELOAD幹掉sleep就好惹

a.c:

```c
void sleep(int a) {
}
```

`gcc -shared -fPIC a.c -o a.so`

`LD_PRELOAD=$PWD/a.so ./timemachine_beta`

跑完就噴FLAG惹

FLAG: vxctf{265160782}
