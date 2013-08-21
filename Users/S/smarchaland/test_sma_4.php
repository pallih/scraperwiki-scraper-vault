<?php
$html = scraperWiki::scrape("http://www.nosdeputes.fr/deputes/tags/actionnaire"); 

print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();
 $dom->load($html);
 foreach($dom->find("div.contenu_page div ul") as $data){ 
 $tds = $data->find("li");
 $record = array( 'depute' => $tds[0]->plaintext);
 scraperwiki::save(array('actionnaire'), $record); 
 }

?>
