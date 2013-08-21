<?php
 
//Get simple_html_dom
require 'scraperwiki/simple_html_dom.php';
 
//Load up Public Whip page
$html = scraperWiki::scrape("http://www.publicwhip.org.uk/division.php?date=2003-03-18&number=118&display=allpossible");                    
$dom = new simple_html_dom();
$dom->load($html);

//For each "tr" in the table marked with the class 'votes', get plaintext stuff and save it
foreach($dom->find("table[@class='votes'] tr") as $data){
    $tds = $data->find("td");
    $MP_long = $tds[0]->plaintext;
    $MP = explode(' ', $MP_long);

        $record = array(
            'MP' => $MP[1] . " " . $MP[2],
            'CONSTITUENCY' => $tds[1]->plaintext,
            'PARTY' => $tds[2]->plaintext,
            'VOTE' => $tds[3]->plaintext
    );
    scraperwiki::save(array('MP'), $record);           
    }

?>
