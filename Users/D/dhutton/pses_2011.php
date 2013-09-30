<?php
$html = scraperWiki::scrape("http://www.tbs-sct.gc.ca/pses-saff/2011/results-resultats/bq-pq/00/org-eng.aspx");
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find(".answertable caption") as $data){
    $record = array(
        '1-question' => $data->plaintext
    );

    scraperwiki::save_sqlite(array('1-question'), $record);
}

?><?php
$html = scraperWiki::scrape("http://www.tbs-sct.gc.ca/pses-saff/2011/results-resultats/bq-pq/00/org-eng.aspx");
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find(".answertable caption") as $data){
    $record = array(
        '1-question' => $data->plaintext
    );

    scraperwiki::save_sqlite(array('1-question'), $record);
}

?>