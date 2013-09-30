<?php

#print "Hello, coding in the cloud!\n";

$html = scraperWiki::scrape("http://baseball.yahoo.co.jp/npb/stats/pitcher?series=2");

#print $html . "\n";

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table > tr") as $data){
    $tds = $data->find("td");
    $record = array(
        'name' => $tds[0]->plaintext, 
        'average' => intval($tds[4]->plaintext)
    );
    print_r($record);
}

scraperwiki::save(array('country'), $record);




?>
<?php

#print "Hello, coding in the cloud!\n";

$html = scraperWiki::scrape("http://baseball.yahoo.co.jp/npb/stats/pitcher?series=2");

#print $html . "\n";

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table > tr") as $data){
    $tds = $data->find("td");
    $record = array(
        'name' => $tds[0]->plaintext, 
        'average' => intval($tds[4]->plaintext)
    );
    print_r($record);
}

scraperwiki::save(array('country'), $record);




?>
