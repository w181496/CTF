# JOI

- 原圖直接decode可以得到
    - `C_F(n1, n2) = 14 * [C(n1,n2) / 14] + 7 * FLAG(n1,n2) + (C(n1,n2) mod 7)`
- 仔細觀察，可以發現圖上不只黑和白
    - 實際上有四種顏色
- 把每種顏色分別拔出來，可以得到以下四種圖:
    - ![](https://github.com/w181496/CTF/blob/master/volgactf2019_quals/JOI/c1.png)
    - ![](https://github.com/w181496/CTF/blob/master/volgactf2019_quals/JOI/c2.png)
    - ![](https://github.com/w181496/CTF/blob/master/volgactf2019_quals/JOI/c3.png)
    - ![](https://github.com/w181496/CTF/blob/master/volgactf2019_quals/JOI/c4.png)

- `C`, `C_F`, `FLAG`可以猜測為三張不同圖片
- `(n1, n2)`代表x和y座標
- 假設原本式子是做整數除法，且每個位置的value只有0~1，那輸出只有4種value很合理
    - 在此假設下，`14 * [C(n1,n2) / 14]`可以直接忽略
    - `FLAG(n1, n2)`就可以直接逆推回去
    - `C_F(n1, n2) = 7 or 8` => `FLAG(n1, n2) = 1`
    - `C_F(n1, n2) = 0 or 1` => `FLAG(n1, n2) = 0`
- 所以抓原圖其中兩個顏色變成1，剩下變成0就可以還原FLAG
- ![](https://github.com/w181496/CTF/blob/master/volgactf2019_quals/JOI/flag.png)
