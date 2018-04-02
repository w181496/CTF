- upload功能能上傳檔案
- 但是會檢查副檔名有沒有出現`h`，有的話就算不合法
    - `stristr(pathinfo($name)["extension"], "h"))`
- 傳其他檔案上去都不能直接訪問，會403，所以就是要想辦法蓋`index.php`
- `move_uploaded_file()`可以覆蓋舊檔案，但是`index.php`副檔名有`h`，要想辦法繞
- 直覺想到以前看過的一招: `index.php/.`
    - 但是這招沒辦法覆寫舊檔案，只能寫新檔案
    - 改用`a/../index.php/.`就能成功覆寫
- 然後翻一下`/var/www/html/flag/`下面，會看到有個檔案`93f4c28c0cf0b07dfd7012dca2cb868cc0228cad`
    - 裡頭是OPcache Byte code
    - 內容乍看之下是在做一連串flag的加解密
    - 大概就猜想可能要去逆向它
    - 於是找到這個Tool有Disassembler: https://github.com/GoSecure/php7-opcache-override
    - 但是踹了很久一直Fail，一開始還要裝特定版本的construct套件
    - 也修正opcache中間少一個NULL Byte的問題，結果還是不行，就卡在這沒解出來Orz
    - 賽後才知道Tool沒處理到某些opcode，要手動修正去逆向的樣子...
    - 修正後可以還原出以下pseudo code:
    ```
    function encrypt() {
      #0 !0 = RECV(None, None);
      #1 !0 = RECV(None, None);
      #2 DO_FCALL_BY_NAME(None, 'mt_srand');
      #3 SEND_VAL(1337, None);
      #4 (129)?(None, None);
      #5 ASSIGN(!0, '');
      #6 (121)?(!0, None);
      #7 ASSIGN(None, None);
      #8 (121)?(!0, None);
      #9 ASSIGN(None, None);
      #10 ASSIGN(None, 0);
      #11 JMP(->-24, None);
      #12 DO_FCALL_BY_NAME(None, 'chr');
      #13 DO_FCALL_BY_NAME(None, 'ord');
      #14 FETCH_DIM_R(!0, None);
      #15 (117)?(None, None);
      #16 (129)?(None, None);
      #17 DO_FCALL_BY_NAME(None, 'ord');
      #18 MOD(None, None);
      #19 FETCH_DIM_R(!0, None);
      #20 (117)?(None, None);
      #21 (129)?(None, None);
      #22 BW_XOR(None, None);
      #23 DO_FCALL_BY_NAME(None, 'mt_rand');
      #24 SEND_VAL(0, None);
      #25 SEND_VAL(255, None);
      #26 (129)?(None, None);
      #27 BW_XOR(None, None);
      #28 SEND_VAL(None, None);
      #29 (129)?(None, None);
      #30 ASSIGN_CONCAT(!0, None);
      #31 PRE_INC(None, None);
      #32 IS_SMALLER(None, None);
      #33 JMPNZ(None, ->134217662);
      #34 DO_FCALL_BY_NAME(None, 'encode');
      #35 (117)?(!0, None);
      #36 (130)?(None, None);
      #37 RETURN(None, None);

    }
    function encode() {
      #0 RECV(None, None);
      #1 ASSIGN(None, '');
      #2 ASSIGN(None, 0);
      #3 JMP(->-81, None);
      #4 DO_FCALL_BY_NAME(None, 'dechex');
      #5 DO_FCALL_BY_NAME(None, 'ord');
      #6 FETCH_DIM_R(None, None);
      #7 (117)?(None, None);
      #8 (129)?(None, None);
      #9 (117)?(None, None);
      #10 (129)?(None, None);
      #11 ASSIGN(None, None);
      #12 (121)?(None, None);
      #13 IS_EQUAL(None, 1);
      #14 JMPZ(None, ->-94);
      #15 CONCAT('0', None);
      #16 ASSIGN_CONCAT(None, None);
      #17 JMP(->-96, None);
      #18 ASSIGN_CONCAT(None, None);
      #19 PRE_INC(None, None);
      #20 (121)?(None, None);
      #21 IS_SMALLER(None, None);
      #22 JMPNZ(None, ->134217612);
      #23 RETURN(None, None);

    }

    #0 ASSIGN(None, 'input_your_flag_here');
    #1 DO_FCALL_BY_NAME(None, 'encrypt');
    #2 SEND_VAL('this_is_a_very_secret_key', None);
    #3 (117)?(None, None);
    #4 (130)?(None, None);
    #5 IS_IDENTICAL(None, '85b954fc8380a466276e4a48249ddd4a199fc34e5b061464e4295fc5020c88bfd8545519ab');
    #6 JMPZ(None, ->-136);
    #7 ECHO('Congratulation! You got it!', None);
    #8 EXIT(None, None);
    #9 ECHO('Wrong Answer', None);
    #10 EXIT(None, None);
    ```
