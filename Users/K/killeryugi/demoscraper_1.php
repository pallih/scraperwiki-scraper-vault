<?php
$html = scraperWiki::scrape("http://www.ohcheri.com/allprods.php");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table.productListing tr") as $data){
    $tds = $data->find("td");
    $record = array(
        'country' => $tds[1]->plaintext, 
        'years_in_school' => $tds[2]->plaintext
    );
    scraperwiki::save(array('country'), $record);
}
?>
