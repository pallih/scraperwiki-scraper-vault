<?php

# Blank PHP
$html = scraperWiki::scrape("http://wolvescivic.co.uk/index.asp?loc=booknow&sort=d&o=0"); 
 
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$i = 1;
foreach($dom->find("div.contentholder2 tr") as $data){
    if ($i > 1) {
        $tds = $data->find("td");
        $record = array(
                'id' => $i,
                'event' => str_replace("´","'",$tds[0]->plaintext), 
                'date' => $tds[1]->plaintext,
                'venue' => $tds[2]->plaintext,
                'status' => $tds[3]->innertext
        );
        scraperwiki::save_sqlite(array('id'), $record);
    }
    $i++;  
}        
?><?php

# Blank PHP
$html = scraperWiki::scrape("http://wolvescivic.co.uk/index.asp?loc=booknow&sort=d&o=0"); 
 
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$i = 1;
foreach($dom->find("div.contentholder2 tr") as $data){
    if ($i > 1) {
        $tds = $data->find("td");
        $record = array(
                'id' => $i,
                'event' => str_replace("´","'",$tds[0]->plaintext), 
                'date' => $tds[1]->plaintext,
                'venue' => $tds[2]->plaintext,
                'status' => $tds[3]->innertext
        );
        scraperwiki::save_sqlite(array('id'), $record);
    }
    $i++;  
}        
?>