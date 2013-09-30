<?php
require 'scraperwiki/simple_html_dom.php';

$i = 17881;
while($i<=29812) {

$html = scraperWiki::scrape("http://www.ellatha.com/eve/LPIndex-" . $i);
$dom = new simple_html_dom();
$dom->load($html);
$a = $i;
foreach($dom->find("tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==6){
        $record = array(
            'Record Num' => intval($a),
            'Faction Corp Name' => $tds[0]->plaintext, 
            'Reward Name' => $tds[2]->plaintext,
            'LP Cost' => $tds[3]->plaintext,
            'Isk Cost' => $tds[4]->plaintext,
            'Required Items' => $tds[5]->plaintext
        );
        scraperwiki::save(array('Record Num'), $record);   
        //print json_encode($record) . "\n";
    $a++;
    }

}

$i = $i + 20;
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';

$i = 17881;
while($i<=29812) {

$html = scraperWiki::scrape("http://www.ellatha.com/eve/LPIndex-" . $i);
$dom = new simple_html_dom();
$dom->load($html);
$a = $i;
foreach($dom->find("tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==6){
        $record = array(
            'Record Num' => intval($a),
            'Faction Corp Name' => $tds[0]->plaintext, 
            'Reward Name' => $tds[2]->plaintext,
            'LP Cost' => $tds[3]->plaintext,
            'Isk Cost' => $tds[4]->plaintext,
            'Required Items' => $tds[5]->plaintext
        );
        scraperwiki::save(array('Record Num'), $record);   
        //print json_encode($record) . "\n";
    $a++;
    }

}

$i = $i + 20;
}

?>
