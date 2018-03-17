wget https://shattered.io/static/shattered-1.pdf

wget https://shattered.io/static/shattered-2.pdf

cat shattered-1.pdf | base64 > payload

cat shattered-2.pdf | base64 >> payload

cat payload - | nc bamboofox.cs.nctu.edu.tw 22006
