<?php 

$html = scraperWiki::scrape("http://traintimes.org.uk/live/orm");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='content'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==4){
        $record = array(
            'Time' => $tds[0]->plaintext,
            'From' => $tds[1]->plaintext,
            //'Platform' => intval($tds[3]->plaintext),
            //'Details' => $tds[3]->plaintext,
            'dateadded' => microtime(true)
            //'Platform' => intval($tds[3]->plaintext)
        );
        scraperwiki::save(array('dateadded'), $record);
    }
}

?>
<?php 

$html = scraperWiki::scrape("http://traintimes.org.uk/live/orm");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='content'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==4){
        $record = array(
            'Time' => $tds[0]->plaintext,
            'From' => $tds[1]->plaintext,
            //'Platform' => intval($tds[3]->plaintext),
            //'Details' => $tds[3]->plaintext,
            'dateadded' => microtime(true)
            //'Platform' => intval($tds[3]->plaintext)
        );
        scraperwiki::save(array('dateadded'), $record);
    }
}

?>
