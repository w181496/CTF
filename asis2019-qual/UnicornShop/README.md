# Unicorn Shop

賽中沒解出來QQ

- fuzzing一波可以發現他行為很詭異
- `imoney>9`的時候，啥都不能買
- id可以`-3`~`4`
- 賽後才知道他`imoney`應該是只吃一個字元，然後轉成數字
- 所以目標就是塞一個字元，想辦法讓轉成數字之後>1069.6
- 這邊就是用一些特殊的unicode字元
    - e.g. `ↁ`, `ↂ`
    - `ASIS{DRaCu1a_hUm4n_Mon57eR_UniC0de_VVh4tEv3r_}`
