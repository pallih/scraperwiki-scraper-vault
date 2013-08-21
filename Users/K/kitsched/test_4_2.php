<?php

$url = 'http://www.whatismyip.org/';

$html = scraperWiki::scrape($url);
echo($html);

?>
