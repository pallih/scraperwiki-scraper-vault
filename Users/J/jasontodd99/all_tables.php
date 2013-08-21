<?php

$html = scraperWiki::scrape("http://www.legis.state.tx.us/BillLookup/History.aspx?LegSess=831&Bill=HB1");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@frame='hsides'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==6){
        $record = array(
            'chamber' => $tds[0]->plaintext, 
            'description' => $tds[1]->plaintext, 
            'comment' => $tds[2]->plaintext,
            'date' => $tds[3]->plaintext,
            'time' => $tds[4]->plaintext,
            'journal' => $tds[5]->plaintext

        );

        scraperwiki::save(array('description'), $record);    
    }
}


?>
