<?php

//Get simple_html_dom.php
require 'scraperwiki/simple_html_dom.php';

$hm = scraperWiki::scrape("http://www.hm.com/es/subdepartment/MEN");                    
$hm_dom = new simple_html_dom();
$hm_dom->load($hm);
$contador=1;
foreach($hm_dom->find("ul[@id='list-products'] li div a[@title]") as $product){
 
    if(count($product)==1){

        print $product->href."\n";  
        $record = array(
            'ID'       => $contador,
            'ARTICULO' => $product->href,
            'ENLACE'   => $product->title);
        scraperwiki::save(array('ID'), $record)

;
    
    $contador = $contador + 1;
    }



};
?>