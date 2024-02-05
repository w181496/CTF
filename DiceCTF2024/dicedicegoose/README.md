# dicedicegoose

題目要求 9 分才會吐 flag

滿足此要求的可能路徑只有一條，即我們角色一直往下走，以及對方一直往左走

Payload:

```
history = [[[0,1],[9,9]],[[1,1],[9,8]],[[2,1],[9,7]],[[3,1],[9,6]],[[4,1],[9,5]],[[5,1],[9,4]],[[6,1],[9,3]],[[7,1],[9,2]],[[8,1],[9,1]]]
encode(history)
> 'AAEJCQEBCQgCAQkHAwEJBgQBCQUFAQkEBgEJAwcBCQIIAQkB'
```

`dice{pr0_duck_gam3r_AAEJCQEBCQgCAQkHAwEJBgQBCQUFAQkEBgEJAwcBCQIIAQkB}`
