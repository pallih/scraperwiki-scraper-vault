<?php

require 'scraperwiki/simple_html_dom.php';
$html = scraperWiki::scrape("http://bc2013.com/candidates"); 
$dom = new simple_html_dom();
$dom->load($html);
// try curl instead of scrape
// print($html);
$counter = 0;
foreach($dom->find("div.entry-content table tr") as $data){
    $tds = $data->find("td");
    //print_r($counter);
    if($counter > 0) {
        if(count($tds)==6){
            $record = array(
                'district' => $tds[0]->plaintext, 
                'liberal' =>$tds[1]->plaintext,
                'ndp' =>$tds[2]->plaintext,
                'green' =>$tds[3]->plaintext,
                'conservative' =>$tds[4]->plaintext,
                'other' =>$tds[5]->plaintext,
            );
            print json_encode($record) . "\n";
            scraperwiki::save(array('district'), $record);
        }
    }
    $counter++;
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';
$html = scraperWiki::scrape("http://bc2013.com/candidates"); 
$dom = new simple_html_dom();
$dom->load($html);
// try curl instead of scrape
// print($html);
$counter = 0;
foreach($dom->find("div.entry-content table tr") as $data){
    $tds = $data->find("td");
    //print_r($counter);
    if($counter > 0) {
        if(count($tds)==6){
            $record = array(
                'district' => $tds[0]->plaintext, 
                'liberal' =>$tds[1]->plaintext,
                'ndp' =>$tds[2]->plaintext,
                'green' =>$tds[3]->plaintext,
                'conservative' =>$tds[4]->plaintext,
                'other' =>$tds[5]->plaintext,
            );
            print json_encode($record) . "\n";
            scraperwiki::save(array('district'), $record);
        }
    }
    $counter++;
}

?>
