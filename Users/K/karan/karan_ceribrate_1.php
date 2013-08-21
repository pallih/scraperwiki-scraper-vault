<?php
$html = scraperWiki::scrape("https://www.google.co.in/#hl=en&q=austere+meaning");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@class='ts'] tr") as $data){
    $tds = $data->find("td");
    
        $record = array(
            'meaning' => $tds[0]->plaintext, 
        );
      scraperwiki::save(array('country'), $record);

    }
?>