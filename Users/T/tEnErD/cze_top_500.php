<?php

require 'scraperwiki/simple_html_dom.php';           
for ($i = 0; $i < 20; $i++) {
    $html = scraperWiki::scrape("http://www.alexa.com/topsites/countries;$i/CZ");           
    
    
    $dom = new simple_html_dom();
    $dom->load($html);
    $position = 0;
    $result = array();
    foreach($dom->find("span[@class='topsites-label']") as $data){
        $result = $data->plaintext;      
        $target = scraperWiki::scrape($result);
        $ga = FALSE;
        if (strpos($target, 'ga.js') !== FALSE) {
            $ga = TRUE;    
        }

        scraperWiki::save_sqlite(array("data"), array('data' => $result, 'ga' => $ga));    
    }
}


?>
