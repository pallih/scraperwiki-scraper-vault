<?php

print "Hello, coding in the cloud!";

$html = scraperWiki::scrape("http://www.hospitalsworldwide.com/listings/2191.php");
//print $html . "\n";


require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div#main") as $dataDetails){
    $dataDetails= $data->find("p");

    print_r($dataDetails);
}

// scraperwiki::save(array('country'), $record);


?>
<?php

print "Hello, coding in the cloud!";

$html = scraperWiki::scrape("http://www.hospitalsworldwide.com/listings/2191.php");
//print $html . "\n";


require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div#main") as $dataDetails){
    $dataDetails= $data->find("p");

    print_r($dataDetails);
}

// scraperwiki::save(array('country'), $record);


?>
