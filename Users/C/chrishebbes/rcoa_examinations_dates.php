<?php

$html = scraperWiki::scrape("http://rcoa.ac.uk/node/300");           
require 'scraperwiki/simple_html_dom.php';   
function print_date($when) {           
    print $when->format(DATE_ISO8601) . "\n"; 
}    
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("tr") as $data){
    $tds = $data->find("td");
if(count($tds)==3){
        print $tds;
        $record = array(
            'title' => $tds[0]->plaintext, 
            'value' => $tds[1]->format(DATE_ISO8601)
        );
        scraperwiki::save(array('title'), $record);
        $record = array(
            'title' => $tds[0]->plaintext, 
            'value' => $tds[2]->plaintext
        ); 
        scraperwiki::save(array('title'), $record); 
    }
}
?>
<?php

$html = scraperWiki::scrape("http://rcoa.ac.uk/node/300");           
require 'scraperwiki/simple_html_dom.php';   
function print_date($when) {           
    print $when->format(DATE_ISO8601) . "\n"; 
}    
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("tr") as $data){
    $tds = $data->find("td");
if(count($tds)==3){
        print $tds;
        $record = array(
            'title' => $tds[0]->plaintext, 
            'value' => $tds[1]->format(DATE_ISO8601)
        );
        scraperwiki::save(array('title'), $record);
        $record = array(
            'title' => $tds[0]->plaintext, 
            'value' => $tds[2]->plaintext
        ); 
        scraperwiki::save(array('title'), $record); 
    }
}
?>
