<?php
            $html = scraperWiki::scrape("https://suojeluskunta.com/forum/");
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==12){
        $record = array(
            'teuvo' => $tds[0]->plaintext, 
            'years_in_school' => intval($tds[4]->plaintext)
        );
        print json_encode($record) . "\n";
    }
}
scraperwiki::save(array('teuvo'), $record);           
?>
<?php
            $html = scraperWiki::scrape("https://suojeluskunta.com/forum/");
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==12){
        $record = array(
            'teuvo' => $tds[0]->plaintext, 
            'years_in_school' => intval($tds[4]->plaintext)
        );
        print json_encode($record) . "\n";
    }
}
scraperwiki::save(array('teuvo'), $record);           
?>
