<?php
require 'scraperwiki/simple_html_dom.php';
$num = 1;
while ( $num <= 3 ) {
    $html = scraperWiki::scrape("http://www.acas.rs/acasPublic/izvestajDetails.htm?parent=pretragaIzvestaja&izvestajId=".$num);
    #$html = scraperWiki::scrape("http://www.acas.rs/acasPublic/izvestajDetails.htm?parent=pretragaIzvestaja&izvestajId=1");
    $num = $num +1;
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div tr") as $data){
        $tds = $data->find("td");
        if(count($tds)> 1){
            $record = array(
                'country' => $tds[0]->plaintext, 
                'country1' => $tds[1]->plaintext,
                'country2' => $tds[2]->plaintext,
                'country3' => $tds[3]->plaintext,
                'country4' => $tds[4]->plaintext
                #'years_in_school' => intval($tds[4]->plaintext)
            );
            scraperwiki::save(array('country'), $record);
        }
    }
}

?>
