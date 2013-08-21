<?php

$html = scraperWiki::scrape("http://www.nosdeputes.fr/deputes/tags/actionnaire"); 

//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();
 $dom->load($html);
 foreach($dom->find("div.contenu_page div ul li") as $data){ 
  $tds = $data->find("a");
  $tdt = $data->find("span");
 $record = array( 'depute' => $tds[0]->plaintext, 'intervention' => $tdt[0]->plaintext,'Mot clés' => 'actionnaire');
 scraperwiki::save(array('depute'), $record);
 }

$html = scraperWiki::scrape("http://www.nosdeputes.fr/deputes/tags/poles de competitivite");

//print $html . "\n";

//require 'scraperwiki/simple_html_dom.php';
// $dom = new simple_html_dom();
 $dom1->load($html);
 foreach($dom1->find("div.contenu_page div ul li") as $data){
  $tds = $data->find("a");
  $tdt = $data->find("span");
 $record = array( 'depute' => $tds[0]->plaintext, 'intervention' => $tdt[0]->plaintext,'Mot clés' => 'poles de competitivite');
 scraperwiki::save(array('depute'), $record);
 }

?>
