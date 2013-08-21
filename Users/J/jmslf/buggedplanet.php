<?php

# Blank PHP

$html = scraperWiki::scrape("http://buggedplanet.info/");

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();
$dom->load($html);

$countries = array();
foreach($dom->find("ul li a") as $data){
    if (preg_match('/^[A-Z]{2}$/', $data->title)){
        $countries[$data->title] = "http://buggedplanet.info" . $data->href;
    }
}

$countries_found = array();
foreach($countries as $code => $href){
    if (/*$code == "LY"*/ true){
        $html = scraperWiki::scrape($href);
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find("h1 span[id=Vendor_Appearance]") as $h1){
            $list = $h1->parent()->next_sibling();
            if ($list->tag == "ul"){    
                            
                foreach($list->children() as $li){
//                    scraperwiki::save_var($code, $li->plaintext);
                    $countries_found[$code] = $li->plaintext;
                    echo $code . " : " . $li->plaintext;
                }
            }
        }
    }
}

print_r($countries_found);


?>
