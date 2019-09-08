# imgur

這題你可以註冊一個使用者

並且可以設定一張來自imgur的圖片當作大頭貼

他會去抓該圖片下來，放到`profiles/xxxxx.jpg`

並且本題還有一個LFI: `?page=xxxx`

所以目標很明顯

塞php code進去圖片，並傳到imgur，接著讓後端載下來圖片，去LFI它，RCE

`DCTF{762241E8981F7E4C2B134C2894747990989FB5DFF0A3AD8DB5A0CEB5D05CBD8D}`

![](https://github.com/w181496/CTF/blob/master/dctf2019-qual/imgur/imgur.png)
