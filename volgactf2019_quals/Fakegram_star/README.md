# Fakegram Star

- 題目給了一個Instagram帳號，說flag藏在裡頭

```
Channel special for you
The main thing is difference
Flag is the puzzle in some posts
Without empty space, hashtags, mentions, links
```

- 從個人檔案敘述中，可以猜測可能要去和原始來源的文字做diff
- ![](https://github.com/w181496/CTF/blob/master/volgactf2019_quals/Fakegram_star/diff.png)
- 經過一連串手動diff和找來源文字，可以組合得到FLAG
- `VolgaCTF{theflagisweaskyoutomakewriteupforthistask}`
