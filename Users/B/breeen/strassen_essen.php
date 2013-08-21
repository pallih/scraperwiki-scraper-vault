<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://onlinestreet.de/strassen/in-Essen/Z.html");
$html = str_get_html($html_content);

foreach ($html->find("td.strasse") as $el) {  
    $_data = explode("<span>", $el->children(0)->innertext);
    $_data[1] = str_replace("</span>", "", $_data[1]);
    $_data[1] = trim($_data[1]);
    
    $_data[0] = iconv("ISO-8859-15", "UTF-8", $_data[0]);
    $_data[1] = iconv("ISO-8859-15", "UTF-8", $_data[1]);
    scraperwiki::save_sqlite(array("Strasse", "PLZ"), array("Strasse" => $_data[0], "PLZ" => $_data[1]));
    //print $_data[0] . "|" . $_data[1] . "\n";
}

?>