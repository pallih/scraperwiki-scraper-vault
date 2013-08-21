<?php

require 'scraperwiki/simple_html_dom.php';

$html_content = scraperwiki::scrape("https://scraperwiki.com/");
$html = str_get_html($html_content);

$i=0;
foreach ($html->find("a") as $el) {

$message = scraperwiki::save_sqlite(array("id"),array("id"=>$i++,"href_text"=>$el->href)); 

}

?>


