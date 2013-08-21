<?php
$html = scraperWiki::scrape("http://www.ebioscience.com/new-products.htm"); 
print $html . "\n"; 
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom(); 
$dom->load($html); 
foreach($dom->find("div[@align='left'] tr") as $data){ $tds = $data->find("td"); 
if(count($tds)==12){ 
$record = array( 
'country' => $tds[0]->plaintext, 
'years_in_school' => intval($tds[4]->plaintext) 
); 
print json_encode($record) . "\n"; 
    } 
}


$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==7){
        $record = array(
            'name' => $tds[0]->plaintext,
            'clone' => $tds[1]->plaintext,
            'application' => $tds[2]->plaintext,
            'cat' => $tds[3]->plaintext,
            'reg' => $tds[4]->plaintext,
            'date' => $tds[5]->plaintext   
        );

        scraperwiki::save(array('name'), $record);
    }
}

?>
