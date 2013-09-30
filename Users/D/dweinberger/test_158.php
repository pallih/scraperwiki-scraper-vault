<?php

$html = scraperWiki::scrape("http://cyber.law.harvard.edu/node/7323");
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("h2") as $data){
    //$url = $data->find("a");
    $record = array(
        'title' => $data->plaintext//,
        //url' => $url->plaintext //
    );

   // scraperwiki::save(array('title'), $record);
}

  


?>

<?php

$html = scraperWiki::scrape("http://cyber.law.harvard.edu/node/7323");
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("h2") as $data){
    //$url = $data->find("a");
    $record = array(
        'title' => $data->plaintext//,
        //url' => $url->plaintext //
    );

   // scraperwiki::save(array('title'), $record);
}

  


?>

