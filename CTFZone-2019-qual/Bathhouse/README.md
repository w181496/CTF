# Bathhouse

超級通靈大爛題

- Step1. /robots.txt
    - 可以找到 `/set_price` 這個 endpoint
    - 會導向到 `/accounts`，是 Django 的 admin 登入介面

- Step2. SQL Injection
    - Book 的地方，name 欄位可以做 Error Based SQL Injection
    - 但有 WAF 掉一堆字元，包含`'`, `"`, `#`, `\n`, ... 等常見字元
    - 不過反斜線 `\` 可以用 
    - 撈一波，可以找到有 Backup 的 admin 明文帳密: `main_admin_user` / `njafnGAJNSGAkn123`

- Step3. wkhtmltopdf
    - `/set_price` 這個 endpoint 可以設定 price，並生成一個 pdf
    - 其中 price 的部分可以塞 `<iframe>` 去做本地讀檔
        - `<iframe src="file:///etc/passwd" width="1000" height="2000">`
    - 但source code路徑猜不到，很多能leak路徑的檔案也沒辦法直接讀
        - `/proc/1` => gunicorn
        - `/proc/self` => wkhtmltopdf
- Step4. /status
    - 最通靈的部分來了，source code路徑寫在`/status`這個endpoint
        - Web app folder: /opt/project/
        - Submodules: task, calculate
    - 而這個endpoint需要自己掃才能找到

- Step5. 讀 Django source code
    - 用 iframe 讀 `/opt/project/calculate/views.py`
        - `# Get sync data by http request.#     syncData('http://syncdata/sync.html'`
    - 接著繼續用 iframe 訪問` http://syncdata/sync.html` 就能拿到flag
- `ctfzone{0190af5705a38115cd6dee6e7d79e317}`

