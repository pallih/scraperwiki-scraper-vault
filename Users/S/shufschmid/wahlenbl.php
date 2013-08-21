<?php
$recordplus = array();
require 'scraperwiki/simple_html_dom.php';         
 $url1 = "http://www.abstimmungen.bl.ch/Wahlen_2013_3/generated/3_";
    $html = scraperWiki::scrape($url1."arlesheim.htm");           
        
        $dom = new simple_html_dom();
        $dom->load($html);
        $table = $dom->find('table width=',36); 
           $titel = "ja";
           foreach($table->find('<tr>') as $tr) 
           {
                
                if($titel == "ja"){
                    $titel = "nein";
                }
                else{

                    $tds = $tr->find("td");
                    $record = array(
                        'Gemeinde' => $tds[0]->plaintext,
                        'Stimmberechtigte' => $tds[1]->plaintext,
                        'gueltige Wahlzettel' => $tds[2]->plaintext,
                        'Total Stimmen' => $tds[3]->plaintext,
                        'leere Stimmen' => $tds[4]->plaintext,
                        'ungueltige Stimmen' => $tds[5]->plaintext,
                        'gueltige Stimmen' => $tds[6]->plaintext,
                        'gueltige Wahlzettel' => $tds[7]->plaintext,
                        'diverse Stimmen' => $tds[8]->plaintext,
                        'Nussbaumer E' => $tds[9]->plaintext,
                        'Schafroth G' => $tds[10]->plaintext,
                        'Weber T' => $tds[11]->plaintext,
                        'number' => $key++);
                    
        
                        scraperwiki::save(array('number'), $record);
                }
       
}
          



?>
