<?php
require 'scraperwiki/simple_html_dom.php';           

for ($i=1500; $i<3000; $i++){
$html = scraperWiki::scrape("http://www.expofeiras.gov.br/calendario-de-eventos/evento/sq_eventos/".$i);
//print $html . "\n";

$dom = new simple_html_dom();
$dom->load($html);
$record=array();
$record["id"]=$i;

foreach($dom->find("div.calenDetalhe h2") as $data){
$record["nome"] = $data->innertext;
}

$j=0;
foreach($dom->find("div.calenDetalhe p") as $data){
$record["dados".$j].= $data;
$j++;
}
print json_encode($record) . "\n";
if(!empty($record["nome"])){
$msg=scraperwiki::save_sqlite(array('id'), $record);
}
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';           

for ($i=1500; $i<3000; $i++){
$html = scraperWiki::scrape("http://www.expofeiras.gov.br/calendario-de-eventos/evento/sq_eventos/".$i);
//print $html . "\n";

$dom = new simple_html_dom();
$dom->load($html);
$record=array();
$record["id"]=$i;

foreach($dom->find("div.calenDetalhe h2") as $data){
$record["nome"] = $data->innertext;
}

$j=0;
foreach($dom->find("div.calenDetalhe p") as $data){
$record["dados".$j].= $data;
$j++;
}
print json_encode($record) . "\n";
if(!empty($record["nome"])){
$msg=scraperwiki::save_sqlite(array('id'), $record);
}
}

?>
