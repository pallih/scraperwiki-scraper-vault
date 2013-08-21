<?php
$target = "http://www.ngx.com/marketdata/settlements/IASETTLE.html";
$file_handle = fopen($target, "r");
# Fetch the file
while (!feof($file_handle))
echo fgets($file_handle, 4096);
fclose($file_handle);
?>
