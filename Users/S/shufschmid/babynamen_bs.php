<?php
$recordplus = array();
require 'scraperwiki/simple_html_dom.php';         
 $key = 0; 
for($zahl=0;$zahl<4952;$zahl=$zahl+25){

    $html = scraperWiki::scrape("https://www.bethesda.ch/basel/spital/babygalerie.html?tx_cabbabygallery_pi1%5Boffset%5D=".$zahl);           
        
        $dom = new simple_html_dom();
        $dom->load($html);
        foreach($dom->find("<tr class=") as $data){
            $tds = $data->find("td");
                if(count($tds)==6){
                $record = array(
                    'name' => $tds[0]->plaintext,
                    'geschlecht' => $tds[1]->plaintext,
                    'gewicht' => $tds[2]->plaintext,
                    'groesse' => $tds[3]->plaintext,
                    'geburtszeit' => $tds[4]->plaintext,
                    'link' => $tds[5]->plaintext,
                    'number' => $key++);
                
    
                    scraperwiki::save(array('number'), $record);
            }
        }
}

?>
<?php
$recordplus = array();
require 'scraperwiki/simple_html_dom.php';         
 $key = 0; 
for($zahl=0;$zahl<4952;$zahl=$zahl+25){

    $html = scraperWiki::scrape("https://www.bethesda.ch/basel/spital/babygalerie.html?tx_cabbabygallery_pi1%5Boffset%5D=".$zahl);           
        
        $dom = new simple_html_dom();
        $dom->load($html);
        foreach($dom->find("<tr class=") as $data){
            $tds = $data->find("td");
                if(count($tds)==6){
                $record = array(
                    'name' => $tds[0]->plaintext,
                    'geschlecht' => $tds[1]->plaintext,
                    'gewicht' => $tds[2]->plaintext,
                    'groesse' => $tds[3]->plaintext,
                    'geburtszeit' => $tds[4]->plaintext,
                    'link' => $tds[5]->plaintext,
                    'number' => $key++);
                
    
                    scraperwiki::save(array('number'), $record);
            }
        }
}

?>
