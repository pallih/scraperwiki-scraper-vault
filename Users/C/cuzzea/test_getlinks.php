<?php

//$html = scraperWiki::scrape("http://forum.softpedia.com/");

/*require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("a") as $data){
    echo($data->href).'
';
}*/

$matches = array();
$pattern = '/[A-Za-z0-9_-.]+@[A-Za-z0-9_-]+\.([A-Za-z0-9_-][A-Za-z0-9_]+)/';
preg_match($pattern,'asd @asd.com vld_a.s@goo.asdfe @asd@google.comIS .asd . er@<2@3gom ',$matches);

var_dump($matches);


?>
<?php

//$html = scraperWiki::scrape("http://forum.softpedia.com/");

/*require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("a") as $data){
    echo($data->href).'
';
}*/

$matches = array();
$pattern = '/[A-Za-z0-9_-.]+@[A-Za-z0-9_-]+\.([A-Za-z0-9_-][A-Za-z0-9_]+)/';
preg_match($pattern,'asd @asd.com vld_a.s@goo.asdfe @asd@google.comIS .asd . er@<2@3gom ',$matches);

var_dump($matches);


?>
