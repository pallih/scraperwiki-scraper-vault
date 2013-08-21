<?php

require 'scraperwiki/simple_html_dom.php';  

$data = file_get_contents("http://www-e.uni-magdeburg.de/jschulen/ocr/gocr-0.49.tar.gz");
file_put_contents("gocr.tar.gz", $data);
exec('tar -xzvf gocr.tar.gz');


?>
