# Darkwebmessageboard

在html source中可以看到以下註解:

`<!-- | Dark Web Message Board | DEVELOPED BY K1tsCr3w | Open source at Kits-AB | -->`

把這串拿去github搜，可以找到這個repo:

https://github.com/kits-ab/the-dark-message-board

快速看一遍code，可以發現登入功能沒做，然後`/board/1`可以看到一串加密訊息:

`rW+fOddzrtdP7ufLj9KTQa9W8T9JhEj7a2AITFA4a2UbeEAtV/ocxB/t4ikLCMsThUXXWz+UFnyXzgLgD9RM+2toOvWRiJPBM2ASjobT+bLLi31F2M3jPfqYK1L9NCSMcmpVGs+OZZhzJmTbfHLdUcDzDwdZcjKcGbwEGlL6Z7+CbHD7RvoJk7Ft3wvFZ7PWIUHPneVAsAglOalJQCyWKtkksy9oUdDfCL9yvLDV4H4HoXGfQwUbLJL4Qx4hXHh3fHDoplTqYdkhi/5E4l6HO0Qh/jmkNLuwUyhcZVnFMet1vK07ePAuu7kkMe6iZ8FNtmluFlLnrlQXrE74Z2vHbQ==`


並且從 github commit 歷史中可以找到production key: https://github.com/kits-ab/the-dark-message-board/commit/d95b029a044491a954b909a280ebebcf6e357ef4#diff-ea209ce78604d811cf3f3771a0f89ea2

對應的 commit message 為: `from some file that reminds me of the song 'here i am something like a hurricane'`

把這段歌詞拿去搜尋，可以發現 `something` 對應的是 `Rock you`

所以目標就是要用`rockyou.txt`去爆密碼

爆出來Password is falloutboy for test.pem

上面那串Decrypted出來是`Bank url: http://bankofsweden-01.pwn.beer`

但80 port連不上，所以用nmap掃一下，就發現5000 port是開的

http://bankofsweden-01.pwn.beer:5000

打開是一個銀行網站，可以註冊登入

但正常註冊會是未驗證使用者，沒辦法登入

仔細觀察一下，會發現有個參數 `is_active`

手動設成1之後就會變成已驗證使用者

成功登入之後，在export功能處，可以發現LFI漏洞

直接下載`app.py`就能看見flag:

`SECFEST{h4ck3r5_60nn4_h4ck_4nd_b4nk3r5_60nn4_cr4ck}`
