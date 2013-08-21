<?php

include("http://davidelks.com/libs/LIB_http.php");
include("http://davidelks.com/libs/LIB_parse.php");

$target = "https://www.google.com/fusiontables/exporttable?query=select+col4+from+3607204+&o=kmllink&g=col4";
$ref = "";

$web_page = http_get($target="http://www.thisisstaffordshire.co.uk/search/search.html?searchPhrase=$keyphrase&searchType=&orderByOption=dateDesc", $referer="");

echo $target;

$kML = http_get ($target, $ref);

?>
