<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.marctracker.com/PublicView/location.jsp");
$html = str_get_html($html_content);

 foreach ($html->find("area") as $el) { 
    $a =  $el->title;
    if (strpos($a,'Train') !== false) {
        echo $a . "\n";
    }         
}
?>
