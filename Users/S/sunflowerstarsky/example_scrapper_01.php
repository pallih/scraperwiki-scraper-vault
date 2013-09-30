<?php

$html = scraperWiki::scrape("http://www.w3schools.com/html/html_tables.asp");
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==12){
        $record = array(
            'fruit' => $tds[0]->plaintext, 
            'how_many' => intval($tds[1]->plaintext)
        );
        // save
        scraperwiki::save(array('fruit'), $record);
        //select * from swdata order by years_in_school desc limit 10
    }
}




?>
<?php

$html = scraperWiki::scrape("http://www.w3schools.com/html/html_tables.asp");
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==12){
        $record = array(
            'fruit' => $tds[0]->plaintext, 
            'how_many' => intval($tds[1]->plaintext)
        );
        // save
        scraperwiki::save(array('fruit'), $record);
        //select * from swdata order by years_in_school desc limit 10
    }
}




?>
