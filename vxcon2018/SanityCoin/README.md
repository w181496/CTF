# Sanity Coin

這題是給大家熟悉smart contract的環境

首先要裝MetaMask才能解這題

看他的smart contract code，可以發現有個匿名函式

當`msg.value == 1984`時，就可以得到一個SanityCoin

而這邊的單位是Wei，所以相當於`0.000000000000001984 ETH`

所以，建立完Smart Contract後

發送`0.000000000000001984 ETH`給Contract Address

就能得到一個Sanity Coin

再來把這個Token加進MetaMask錢包再去Verify就能拿到FLAG

`vxctf{toO_Th3_moooooon_in_2047}`
