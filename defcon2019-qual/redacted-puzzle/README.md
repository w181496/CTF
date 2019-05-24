# Redacted puzzle

[English Version](https://balsn.tw/ctf_writeup/20190513-defconctfqual/#misc)

這題給我們一個gif圖片

把每個frame拔出來，然後用stegsolver去看，調一下可以看到類似這樣子的多邊形:

![](https://raw.githubusercontent.com/w181496/CTF/master/defcon2019-qual/redacted-puzzle/0.png)

![](https://raw.githubusercontent.com/w181496/CTF/master/defcon2019-qual/redacted-puzzle/1.png)

![](https://raw.githubusercontent.com/w181496/CTF/master/defcon2019-qual/redacted-puzzle/2.png)

...

第一張Frame更直接告訴我們Flag alphabet

<br>

仔細觀察，可以發現這些多邊形有一些特性，例如邊長似乎只有固定幾種長度

最後猜測，他很有可能是從某個正多邊形(8邊形)去抓幾個點，然後連線畫出這些圖的

把以上線索拼湊之後，可以發現原型應該是個正八邊形

![](https://raw.githubusercontent.com/w181496/CTF/master/defcon2019-qual/redacted-puzzle/ori.png)

![](https://raw.githubusercontent.com/w181496/CTF/master/defcon2019-qual/redacted-puzzle/ori2.png)

![](https://raw.githubusercontent.com/w181496/CTF/master/defcon2019-qual/redacted-puzzle/ori3.png)


把正八邊形抓的點當作1，沒抓的點當0，然後從左上角開始順時針看

可以發現前幾張圖構成以下的bit string:

0.png: `10001100`

1.png: `01100011`

...

其中`10001` =  `17` 重複出現了三次

而 `alphabet[17] = 'O'`

所以很明顯這就是FLAG

把每張圖抓的bit抓出，然後每五個bit去alphabet抓字元就行惹

然後要稍微注意的是，每個圖形會稍微逆時針旋轉，愈到後面，抓的起點就不一定是最左上角

`OOO{FORCES-GOVERN+TUBE+FRUIT_GROUP=FALLREMEMBER_WEATHER}`
