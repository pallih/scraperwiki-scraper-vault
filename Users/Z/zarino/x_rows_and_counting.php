<?php

require 'scraperwiki/simple_html_dom.php'; 
date_default_timezone_set('Europe/London'); 

$html = scraperwiki::scrape("https://scraperwiki.com/");
$datetime = date("Y-m-d H:i:s", time());
         
$dom = str_get_html($html);

$raw = preg_replace('/[^0-9]/i', '', $dom->find("#shhhh", 0)->plaintext);

scraperwiki::save_sqlite(array('rows'), array("rows"=>$raw,"datetime"=>$datetime));

?>
