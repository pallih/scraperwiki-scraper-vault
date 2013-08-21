<?php
$sourcescraper = '';
$id = isset($_GET['id'])?$_GET['id']:0;
scraperwiki::attach("s-in-s-noidung", "src");
$src = scraperwiki::select("* from src.swdata limit $id,1");
 $title = mb_convert_encoding(base64_decode($src[0]['title']),'utf-8','gbk');
 $content = mb_convert_encoding(base64_decode($src[0]['content']),'utf-8','gbk');
 $url = $src[0]['url'];
 $num = $src[0]['num'];
 $reply = $src[0]['reply'];  
 $order = $src[0]['order'];   
 
?>
<!DOCTYPE html> 
<html> <head> <title>My Collection</title> 
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"> 
<meta charset="UTF-8">
</head>
<body>
<div class="title"><?php echo $title; ?></div>
<div class="content"><?php echo $content; ?></div>
<div class="url"><?php echo $url; ?></div>
<div class="num"><?php echo $num ?></div>
<div class="reply"><?php echo $reply ?></div>
<div class="order"><?php echo $order ?></div>
</body>
</html>
