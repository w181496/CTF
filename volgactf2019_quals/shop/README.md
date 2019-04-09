# shop

- `robots.txt`可以發現有war包可以下載
- 載回來unzip可以得到網站整個classes
- 逆回java後，可以觀察到`ShopController`的部分，用了`@ModelAttribute`
    - `public String buy(@RequestParam Integer productId, @ModelAttribute(value="user") User user, RedirectAttributes redir, HttpServletRequest request)`
    - 所以這邊存在Autobinding的漏洞
    - 我們可以在當前連線覆寫掉`user`的屬性，例如`balance`
- Payload
    - `/buy`
    - POST: `?Balance=1000000&ProductId=4`
