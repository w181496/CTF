# letschat

[English version](README_en.md)

打開題目是一個簡單聊天室

可以創建 room , invite 其他人進來 room, 離開 room, 傳訊息等基本功能

其中 message 和使用者都會有 UUID

經過一連串常見漏洞的嘗試之後，開始把目標轉到 UUID 身上

猜測 flag 可能是最早的 message，所以目標變成想辦法預測 UUID (推算最早的 message UUID)

但這邊還有一些不確定的問題，就是我們不確定拿到 message UUID 後，看不看得到內容 (因為主辦方在開賽沒多久就把所有message censor掉了)

```
"8cefa1c9-e6b8-11eb-92ce-9678c088ab04",
"29563aca-e6b6-11eb-9805-362ad9a78588",
"e3995f2a-e6b5-11eb-9805-362ad9a78588",
"d6d993ba-e6b5-11eb-88a1-a2a63078d4f6",
"0936b5f5-e6b5-11eb-88a1-a2a63078d4f6",
"076ce879-e6b5-11eb-88a1-a2a63078d4f6",
"eeeb9a98-e6b3-11eb-9805-362ad9a78588",
"d093f012-e6b3-11eb-92ce-9678c088ab04",
"bad4e9eb-e6b3-11eb-88a1-a2a63078d4f6",
"6e37099e-e6b3-11eb-86e4-7253a5121377",
"1db54013-e6b3-11eb-9805-362ad9a78588",
"f82847c7-e6b2-11eb-9805-362ad9a78588",
"f2d93fb8-e6b2-11eb-92ce-9678c088ab04",
"f0c5a0c0-e6b2-11eb-88a1-a2a63078d4f6",
"ebb23201-e6b2-11eb-92ce-9678c088ab04"
```

可以觀察到，UUID 後半基本上只有四種組合:

```
11eb-92ce-9678c088ab04
11eb-86e4-7253a5121377
11eb-9805-362ad9a78588
11eb-88a1-a2a63078d4f6
```

而剩下的前半會根據時間做變動

狂炸一波 message 後，發現 message 的 UUID 有點謎：

```
"a7e216c3-e6f3-11eb-88a1-a2a63078d4f6"
"a7e216c8-e6f3-11eb-88a1-a2a63078d4f6"
"a7e216cb-e6f3-11eb-88a1-a2a63078d4f6"
"a7e216cf-e6f3-11eb-88a1-a2a63078d4f6"
"a7e216d1-e6f3-11eb-88a1-a2a63078d4f6"
"a8280d5d-e6f3-11eb-86e4-7253a5121377"
"a8280d63-e6f3-11eb-86e4-7253a5121377"
"a8280d68-e6f3-11eb-86e4-7253a5121377"
"a8280d6a-e6f3-11eb-86e4-7253a5121377"
"a8280d6d-e6f3-11eb-86e4-7253a5121377"
"a82be59c-e6f3-11eb-92ce-9678c088ab04"
"a82be5a0-e6f3-11eb-92ce-9678c088ab04"
"a82be5a2-e6f3-11eb-92ce-9678c088ab04"
"a82be5a6-e6f3-11eb-92ce-9678c088ab04"
"a82be5a8-e6f3-11eb-92ce-9678c088ab04"
"a81d9eb7-e6f3-11eb-9805-362ad9a78588"
"a81d9eba-e6f3-11eb-9805-362ad9a78588"
"a81d9ebf-e6f3-11eb-9805-362ad9a78588"
"a81d9ec1-e6f3-11eb-9805-362ad9a78588"
"a81d9ec2-e6f3-11eb-9805-362ad9a78588"
```

以上 UUID 都是在 1~2 秒內送出的 message 拿到的

可以觀察到當第一個 Byte 固定時，可以分為兩種狀況

1. 後半Pattern不同(四種組合)，則 2~4 Bytes 都會不同
2. 後半Pattern相同，則只有第 4 Byte 會變化

所以大膽猜測第 1 Byte是 Timestamp 秒數，第 4 Byte 可能是毫秒之類的 (在同一秒內會隨時間遞增)

然後就開始挑個跟admin差不多時間點的 UUID，去炸他的第 4 Byte

不意外的，基本上炸到的都是被censor掉的使用者訊息：`<Player> *******`

但發現，第 4 Byte 剛好炸出來有一個訊息沒被 censor 掉：`AzureDiamond:awesome!`

接著繼續多炸幾個，發現當秒數不同時，第 4 bytes 在某個值都會有一個沒被 censor 掉的訊息

```
AzureDiamond:awesome!
(https://letschat-messages-web.2021.ctfcompetition.com/a8280d56-e6f3-11eb-86e4-7253a5121377)

Cthon98:hey, if you type in your pw, it will show as stars
(https://letschat-messages-web.2021.ctfcompetition.com/8cefa1c3-e6b8-11eb-92ce-9678c088ab04)
```

查了一下之後，發現這篇 https://knowyourmeme.com/memes/hunter2 有一模一樣的台詞 (ptt密碼梗)

原本還以為是無聊的彩蛋，結果炸一炸後發現：

`Cthon98:er, I just copy pasted YOUR ******'s and it appears to YOU as FLAG_PART_7_FINAL_PART[flag}] cause its your pw`

flag 居然疑似被拆成多段，放進去這個密碼梗裡面

結論，每秒會有一句密碼梗台詞在輪 (輪完會loop)，flag 被拆成很多段，放進去其中一句台詞

開炸

```
FLAG_PART_1[ctf{chat] 
FLAG_PART_2[your] my FLAG_PART_3[way]-ing FLAG_PART_4[to] 
FLAG_PART_5[the] 
FLAG_PART_6[winning] 
FLAG_PART_7_FINAL_PART[flag}]
```

=>

`CTF{chatyourwaytothewinningflag}`



