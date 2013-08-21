<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';  


$html = scraperWiki::scrape("http://justpaste.it/111f");         
$dom = new simple_html_dom();
$dom->load($html);
$list = $dom->find("ul");
$list = $list[0];
foreach ($list->children as $li) {
    $url = "http://en.wikipedia.org".$li->children(0)->href;
    $html = scraperWiki::scrape($url);  
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("table[@class='infobox vcard']") as $data){
        $trs = $data->find("tr");
        $id = 0;
        $record = array('wiki' => htmlentities($url));
        foreach ($trs as $tr) {
            if ($id == 0) {
                $record['name'] = htmlentities($tr->children(0)->innertext); 
            }
            if ($id == 1 && (count($tr->children(0)->children) > 0) && ($tr->children(0)->children(0)->getAttribute("class") == "image")) {
                $record['image'] = htmlentities($tr->children(0)->children(0)->children(0)->src);
            }
            if ($id > 2 && count($tr->children) == 2) {
                $record[$tr->children(0)->plaintext] =  htmlspecialchars($tr->children(1)->plaintext, ENT_COMPAT , 'UTF-8');
            }
            $id++;
        }
        
        if (array_key_exists('name', $record) && array_key_exists('Location', $record)) {
            scraperwiki::save(array('name', 'Location'), $record); 
        }
            
        
    }
}



?>
