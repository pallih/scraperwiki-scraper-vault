<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

    $dom = new simple_html_dom();
        
    for($pincode=500001;$pincode<=500100;$pincode++){

    $html = scraperWiki::scrape("www.pin-code.co.in/pin-code-search/".$pincode."/");
                   
    $dom->load($html);
    //print ($id);
    $title = $dom->find("title");
    $area = $title[0]->innertext;
    
    $record["pincode"]=$pincode;
    $record["area"] = $area;
    print_r($record);
    scraperwiki::save_sqlite(array("pincode"),$record,"pincodes");

    }
    $dom->__destruct();
    
?>
<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

    $dom = new simple_html_dom();
        
    for($pincode=500001;$pincode<=500100;$pincode++){

    $html = scraperWiki::scrape("www.pin-code.co.in/pin-code-search/".$pincode."/");
                   
    $dom->load($html);
    //print ($id);
    $title = $dom->find("title");
    $area = $title[0]->innertext;
    
    $record["pincode"]=$pincode;
    $record["area"] = $area;
    print_r($record);
    scraperwiki::save_sqlite(array("pincode"),$record,"pincodes");

    }
    $dom->__destruct();
    
?>
