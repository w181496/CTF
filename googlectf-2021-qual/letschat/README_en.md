### letschat

This challenge is a simple chatroom website.
We can do some basic operations, such as creating a chat room, sending a message to the chat room, inviting others to the chat room, etc.


Every message sent and every user will be assigned a **UUID**.

Since the challenge did not tell us where the flag is, we naturally went to the `admin`/`flag` user or `admin`/`flag` chat room to try.
But after a series of common vulnerabilities testing, there was no result, so I started to turn the target to UUID.


We started to guess that the flag might be the earliest message, so the goal was to find a way to predict the UUID (estimate the UUID of the earliest message).


But there are still some uncertain issues here, that is, we are not sure that after we get the message UUID, we can see the content or not. (Because the organizer replaced all the messages to `<Player> *******` shortly after the start of the game.)

We tried to send a large number of messages first and observe the rules of the UUID obtained:

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

It can be observed that there are only four combinations in the latter half of UUID:

```
11eb-92ce-9678c088ab04
11eb-86e4-7253a5121377
11eb-9805-362ad9a78588
11eb-88a1-a2a63078d4f6
```

The remaining first half will be changed according to timestamp.

So, we tried to send a large number of messages in 1~2 seconds, and got the following UUIDs:

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

It can be observed that when the first byte is fixed, it can be divided into two situations:

1. If the second half of the pattern is different, then 2~4 Bytes will be different.
2. If the second half of the pattern is the same, only the 4th Byte will change.

So boldly guess that the first byte is timestamp seconds, and the fourth byte may be milliseconds. (Because in the same second, it will increase with time)

Since we were able to obtain the UUID of other users, I got the UUID of the admin, and then tried to bruteforce the fourth byte of the UUID.

Not surprisingly, most of the messages obtained are `<Player> *******`.

But something incredible happened! There happened to be a message in it that was not replaced: `AzureDiamond:awesome!`.

Then keep testing and found that when the number of seconds is different, there will be a message that has not been replaced when the 4th byte is at a certain value:

```
AzureDiamond:awesome!
(https://letschat-messages-web.2021.ctfcompetition.com/a8280d56-e6f3-11eb-86e4-7253a5121377)

Cthon98:hey, if you type in your pw, it will show as stars
(https://letschat-messages-web.2021.ctfcompetition.com/8cefa1c3-e6b8-11eb-92ce-9678c088ab04)
```

After googling it, I found that this https://knowyourmeme.com/memes/hunter2 has exactly the same words.

I thought it was a boring easter egg, but after continuing to bruteforce, I found out:

```
Cthon98:er, I just copy pasted YOUR ******'s and it appears to YOU as FLAG_PART_7_FINAL_PART[flag}] cause its your pw
```

The flag seems to be broken into multiple paragraphs, put them in these sentences!

So far, I have come to a conclusion that there will be a sentence every second, and part of the flag will be put into one of the sentences.

Finally, start to brute force the fourth byte of a large number of UUIDs to get all the flag fragments:

```
FLAG_PART_1[ctf{chat] 
FLAG_PART_2[your] my FLAG_PART_3[way]-ing FLAG_PART_4[to] 
FLAG_PART_5[the] 
FLAG_PART_6[winning] 
FLAG_PART_7_FINAL_PART[flag}]
```

=>

`CTF{chatyourwaytothewinningflag}`


#### Failed attempts

- Register `admin`, `admiN`, `admin%00`, ...
    - `Error 1062: Duplicate entry 'admiN' for key 'PRIMARY'`
- Leak information by inserting some weird characters.
    - leak mysql column name by inserting `\xff` to parameter:
        - `Error 1366: Incorrect string value: '\xFF' for column 'room_id' at row 1`
        - `Error 1366: Incorrect string value: '\xFF' for column 'username' at row 1`
    - unhandled response(?)
        - `roomName=admin%ff` => `Unhandled response from Scan() on login`
- Tried to truncate query statement by `;`
    - We found that if we insert `;` to the parameters, there is very weird behavior like this:
        - `username=;meowmeow&password=meow` => `Empty username or password`
- Case insensitive on joining a room by room name
    - After trying, we found that if we have been invited to some room like `balsn`, then we can join this room with `Balsn`, `bALSn`, `balSN`, ... (case insensitive).
    - So we tried to create rooms like `admiN`, `admiN%00`, `admiN%20`, ..., then invite ourselves to join `admin` room, but failed.
- Login as `AzureDiamond`
    - I tried the username `AzureDiamond` with password `hunter2`, then successfully login into this account but nothing was found.

