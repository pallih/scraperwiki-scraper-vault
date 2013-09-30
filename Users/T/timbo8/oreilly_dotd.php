<?php

$html = scraperWiki::scrape("http://oreilly.com");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("span[@style='display:block; overflow:hidden;'] ") as $data){
    $as = $data->find("a");
    $h3s = $data->find("h3");
    $time = time();
    $record = array(
        'time' => $time,
        'book' => $as[0]->plaintext,
        'price' => $h3s[0]->plaintext,
    );


     scraperwiki::save(array('book'), $record);
}

?>
<?php

$html = scraperWiki::scrape("http://oreilly.com");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("span[@style='display:block; overflow:hidden;'] ") as $data){
    $as = $data->find("a");
    $h3s = $data->find("h3");
    $time = time();
    $record = array(
        'time' => $time,
        'book' => $as[0]->plaintext,
        'price' => $h3s[0]->plaintext,
    );


     scraperwiki::save(array('book'), $record);
}

?>
