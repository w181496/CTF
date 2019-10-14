# Bounty Pl33z

這題擋了很多東西: 

- `"` 只能出現一次
- `'` 只能出現一次
- 可以用 ``` ` ```
- 不能用 `.`, `/`, `\\`, `<`

隊友@Bookgin fuzzing 出 `-->` 放在開頭不會噴 Error

所以結合 `\u2028` 就能 XSS:

`"%2balert(1)%e2%80%a8-->`

其實這個情境跟 Cure53 的 XSS Challenge level 8 幾乎一模一樣XD

https://github.com/cure53/XSSChallengeWiki/wiki/prompt.ml#level-8
