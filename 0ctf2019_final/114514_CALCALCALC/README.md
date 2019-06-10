# 114514 CALCALCALC

這題跟 RCTF calcalcalc 基本上差不多

不過他改了一些地方

原本的正規表達式限制:

```
if (!/^[0-9a-z\[\]\(\)\+\-\*\/ \t]+$/i.test(str)) {
    return false;
}
```

被改成:

```
if (str !== "114+514") {
    return false;
}
```

然後 backend-python 的 app.py 改成:

`#del __builtins__['exec']`

其他的話還有一些小地方被改掉，例如:

controller的`bson.serialize`換成`JSON.stringify`、`bson.deserialize(p.data)`換成`JSON.parse(p.data)`

所以這題在最一開始就被 `str !== "114+514"` 擋死死的

要找其他方法繞掉這個判斷

後來 fuzzing 發現: 

`{"__proto__":null, "expression": "114+514", "isVip":true}` => 噴500

`{"__proto__":{"constructor":"a"}, "expression": "114+514", "isVip":true}` => 噴500

`{"__proto__":{"constructor":false}, "expression": "114+514", "isVip":true}` => OK

猜測應該能 Prototype Pollution 搞事

最後 fuzzing 出:

`{"__proto__":{"constructor":null},"expression":"5278123+1", "isVip":true}` 這樣就能繞掉

但確切原因不知道為啥XDD

繞掉之後，由於他這次可能有把 timeout 問題處理好，所以原本的 python time-based 解法無法使用

後來 [@bookgin](https://github.com/BookGin) 想到一種可以通用三種語言的 payload: `"${sleep(1)}"`

在node.js、python裡是單純字串，可以對PHP來說他會去跑`sleep(1)`

同理，我們也可以跑任意php code

這邊一樣用 time-based 去慢慢撈 flag 就行

`flag{114 514 1919 810 is a magic bumber}`

