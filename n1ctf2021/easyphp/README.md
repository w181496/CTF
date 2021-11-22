# easyphp

https://github.com/php/php-src/blob/PHP-7.1/ext/phar/phar.c#L1714

從這邊可以看到 phar:// 其實會對 tar 檔案去做 parse，然後會對 `.phar/.metadata` 去反序列化

但這題難點跟0ctf 1linephp有點像，開頭和結尾都會被塞垃圾，讓反序列化失敗

並且，因為tar結構跟zip不太一樣，所以沒有directory機制可以offset指來指去

不過有趣的是，tar檔案最開頭其實是檔名

所以解法就是，算好會塞進去的垃圾長度，接著把生好的tar檔開頭拔掉這個長度的內容即可

