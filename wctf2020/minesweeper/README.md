# minesweeper

比賽第二天時，因為沒啥好玩的題目能看了

所以在隊友勸說之下，勉強看了一下這題

結果意外尻出非預期解，全場(非現場賽)只有三隊解XDD

<br>

首先這題原本是給一個 minesweeper 的噁爛 rust binary

所以大家一直認為這題是個 reverse 題

但到第二天丟提示，提示直接就赤裸裸地放 source code....WTF

所以我們就開始想也許這題其實 Misc 之類的題目

<br>

大概講一下這題架構

他題目包了一個 rdp 連線設定檔

直接 rdp 連上去伺服器後，會開 minesweeper 程式，要過關才會噴flag ((但整張地圖都是地雷，賽中的機率爆幹小

有趣的是他 rdp 是用 window mode，所以我們看不到完整的 rdp 桌面環境，只看得到 minesweeper 這隻視窗程式

<br>

然後我就開始想，會不會這邊可以直接尻爛 rdp

所以我就踹了很多方法

例如把設定檔中的執行檔名字，改成 cmd.exe, notepad.exe 之類的

或是踹一下有沒有開其他port可以用他給的帳密搞事之類的

甚至思考能不能透過 rdp 去做 race condition

但最後都沒啥效果

<br>

過了一會，看到現場賽一堆對岸同胞解開這題

我突然靈光一閃，腦袋中有個聲音告訴我要按shift五下

於是相黏鍵視窗就彈出來惹！！

然後戳一戳可以叫出設定視窗

到 App&features 這邊選 Program feature 之類的選項就能叫出 explorer 了！

最後在 `C:\tmp\flag` 得到 flag XDD

(到比賽結束前，我一直以為這是預期解，想說這題也太惡意了吧，給一個完全沒用到的binary XDDD)

![](https://github.com/w181496/CTF/blob/master/wctf2020/minesweeper/wctf.png)
