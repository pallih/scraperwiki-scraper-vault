<?php

# Learning ScaperWiki

$html = scraperWiki::scrape("http://news.bbc.co.uk/sport1/hi/football/eng_prem/table/default.stm");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("tr.r2") as $rows) {
    $cells = $rows->find("td");
    $record = array(
        'position' => $cells[0]->plaintext,
        'team' => $cells[1]->plaintext,
        'points' => $cells[14]->plaintext 
        );

    scraperwiki::save(array('team'), $record); 
}

foreach($dom->find("tr.r1") as $rows) {
    $cells = $rows->find("td");
    $record = array(
        'position' => $cells[0]->plaintext,
        'team' => $cells[1]->plaintext,
        'points' => $cells[14]->plaintext
        );
    scraperwiki::save(array('team'), $record);
}

?>
<?php

# Learning ScaperWiki

$html = scraperWiki::scrape("http://news.bbc.co.uk/sport1/hi/football/eng_prem/table/default.stm");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("tr.r2") as $rows) {
    $cells = $rows->find("td");
    $record = array(
        'position' => $cells[0]->plaintext,
        'team' => $cells[1]->plaintext,
        'points' => $cells[14]->plaintext 
        );

    scraperwiki::save(array('team'), $record); 
}

foreach($dom->find("tr.r1") as $rows) {
    $cells = $rows->find("td");
    $record = array(
        'position' => $cells[0]->plaintext,
        'team' => $cells[1]->plaintext,
        'points' => $cells[14]->plaintext
        );
    scraperwiki::save(array('team'), $record);
}

?>
