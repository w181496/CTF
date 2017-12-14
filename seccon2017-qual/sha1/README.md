# SHA-1 is dead


https://shattered.io/

Download the two pdf files.

They have same sha1 value.


Because we need 2017 ~ 2018 KB,

So let's add some chars to the files.


`perl -e 'print "A"x14000' >> ./shattered-1.pdf`

`perl -e 'print "A"x14000' >> ./shattered-2.pdf`


Then they still have same sha1 but different sha256.


`SECCON{SHA-1_1995-2017?}`
