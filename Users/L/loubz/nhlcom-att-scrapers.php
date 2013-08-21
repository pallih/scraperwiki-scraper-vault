<?php

require 'scraperwiki/simple_html_dom.php';           
$html;
for($i=1; $i<18; $i++) {
    $html .= scraperWiki::scrape("http://www.nhl.com/ice/playerstats.htm?fetchKey=20132ALLFAFALL&viewName=summary&sort=points&pg=" . $i);        
}

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@class='data'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==19){
        $record = array(
            'name' => $tds[1]->plaintext, 
            'team' => $tds[2]->plaintext, 
            'gp' => $tds[4]->plaintext,
            'g' => $tds[5]->plaintext, 
            'a' => $tds[6]->plaintext,
            'pts' => $tds[7]->plaintext
        );
        scraperwiki::save(array('name'), $record);           
    }
}


?>
