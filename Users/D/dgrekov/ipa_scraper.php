<?php
    require 'scraperwiki/simple_html_dom.php';

for($i = 0; $i< 1000; $i++){
    $html = scraperWiki::scrape("http://www.ipaschools.com/catalog/product_info.php?products_id=$i");           
    
           
    $dom = new simple_html_dom();
    $dom->load($html);
        $name = $dom->find('.pageHeading');
        if(!isset($name[0])){ continue; }
        $record = array(
            'name' => $name[0]->innertext,
            'num' =>$i
        );
        scraperwiki::save(array('num'), $record); 
    

}

?>
