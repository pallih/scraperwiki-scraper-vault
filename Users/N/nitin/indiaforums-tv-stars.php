<?php

//scraperwiki::sqliteexecute("drop table if exists swdata"); 
require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.india-forums.com/television_celebrity_index.asp");
$html = str_get_html($html_content);

print $html_content;
?>