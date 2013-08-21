<?php

$urls = array('http://www.internetretailer.com/top500/list/',
'http://www.internetretailer.com/top500/list/?page=2',
'http://www.internetretailer.com/top500/list/?page=3',
'http://www.internetretailer.com/top500/list/?page=4',
'http://www.internetretailer.com/top500/list/?page=5');

require 'scraperwiki/simple_html_dom.php';  

foreach($urls as $url) {

    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $data = $dom->find(".listing .listing_header");
    
    
    foreach($data as $item){
    
    
        $record = array(
            'name' => $item->children(1)->first_child()->plaintext,
            'category' => $item->children(2)->plaintext,
        );
    
        scraperwiki::save(array('name'), $record);   
    }
}
         
?>
