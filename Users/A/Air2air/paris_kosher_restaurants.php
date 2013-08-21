<?php

$html = scraperWiki::scrape
("http://www.postgresql.org/docs/9.1/static/index.html
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("h1") as $data){
    $tds = $data->find("p");
    if(count($tds)==12){
        $record = array(
            'title' => $tds[0]->plaintext, 
            'content' => intval($tds[4]->plaintext)
        );
scraperwiki::save(array('title'), $record);
    }
}

?>
