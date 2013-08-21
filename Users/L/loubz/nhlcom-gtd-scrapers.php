<?php

require 'scraperwiki/simple_html_dom.php';           
$html;
for($i=1; $i<4; $i++) {
    $html .= scraperWiki::scrape("http://www.nhl.com/ice/playerstats.htm?fetchKey=20132ALLGAGALL&viewName=summary&sort=wins&pg=" . $i);        
}

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@class='data'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==18){
        $record = array(
            'name' => $tds[1]->plaintext, 
            'team' => $tds[2]->plaintext, 
            'gp' => $tds[3]->plaintext,
            'w' => $tds[5]->plaintext,
            'ot' => $tds[7]->plaintext,
            'so' => $tds[13]->plaintext,
            'g' => $tds[14]->plaintext, 
            'a' => $tds[15]->plaintext
        );
        scraperwiki::save(array('name'), $record);           
    }
}


?>
