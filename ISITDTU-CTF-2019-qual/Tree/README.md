# Tree

用steghide可以解出另一張圖片

`steghide extract -sf Tree.jpg`

密碼是`mouse` (根據題目給的敘述+通靈)

會解出一張TreeTree.jpg

![](https://github.com/w181496/CTF/blob/master/ISITDTU-CTF-2019-qual/Tree/TreeTree.jpg)

就是一棵霍夫曼樹

把每個字元對應的binary列出來:

```
d: 0000
t: 00010
s: 00011
{: 001
h: 0100
}: 0101
6: 0110
a: 01110
i: 01111
e: 100
f: 101000
b: 101001
u: 10101
_: 1011
l: 110
!: 111
```

然後可以發現那張TreeTree.jpg還有藏一個文字檔:

`steghide extract -sf TreeTree.jpg`

會解出flag.txt:

```
K`~CHK~a%dK`~0DK~araK~a%eK`~0CK~arZK`~0CK`~0CK~araK`~CGK~arZK~arZK`~CGK`~CGK`~0DK~a%eK`~0CK~a%eK`~CHK`~CHK~a%dK`~0DK~a%dK~a%eK`~CGK`~CHK`~0CK~a%eK`~CGK~araK`~0CK~arZK~a%eK~a%dK~arZK`~CGK~araK~a%dK~araK~araK~arZK~a%dK`~CHK`~0DK~araK`~CHK~a%eK~a%eK~a%eK~a%eK`~CGK~7
```

其內容可以發現有一定規律性，可以每5個一組分成下面這樣子:

```
K`~CH
K~a%d
K`~0D
K~ara
K~a%e
K`~0C
K~arZ
K`~0C
K`~0C
K~ara
K`~CG
K~arZ
K~arZ
...
```

由於flag為`isitdtu{`開頭，根據霍夫曼樹換成binary是: `011110001101111000100000000101010100...`

接著比對這串跟flag.txt的關係，再通靈請神一下

會發現可以把binary每3個拆開來，對應到flag.txt每五個一組的其中一組

整理一下可以列出這樣的對應:

```
K`~0C => 000
K`~CH => 011
K~a%d => 110
K`~0D => 001
K~ara => 101
K~a%e => 111
K~arZ => 100
K`~CG => 010
```

寫個腳本喇一下:

```python
with open("flag.txt", "r") as f:
    d = f.read().strip()

x = ''

dic = {'K`~0C':'000', 'K`~CH': '011', 'K~a%d': '110', 'K`~0D':'001', 'K~ara': '101', 'K~a%e': '111', 'K~arZ': '100', 'K`~CG': '010'}
dic2 = {'d': '0000','t': '00010','s': '00011','{': '001','h': '0100','}': '0101','6': '0110','a': '01110','i': '01111','e': '100','f': '101000','b': '101001','u': '10101','_': '1011','l': '110','!': '111'}


for i in range(len(d) / 5):
    s = d[5 * i : 5 * (i + 1)]
    x += dic[s]

print(x)

ans = ''
i = 0
while i < len(x):
    for a, b in dic2.items():
        l = len(b)
        if x[i: i+l] == b:
            ans += a
            print(ans)
            i += (l )
            break
```

flag: `isitdtu{this_is_beautiful_6666_!!!!}`

覺得靈力又上升了一點
