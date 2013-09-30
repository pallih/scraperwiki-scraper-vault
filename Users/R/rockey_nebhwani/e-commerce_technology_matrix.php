<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://builtwith.com/target.com");
$html = str_get_html($html_content);

foreach ($html->find("div.grid_8 div") as $techdiv) {
  //print_r($tech) ;
  //foreach ($el->find("div.pT strong") as $tech){
  //  print_r($tech);
  //  print $tech->innertext . "\n";   
  //}
  //$tech = $el->find("strong"); 
  
  print $techdiv->innertext . "\n";
  //$record = array( 'tech' => $tech[4]->plaintext); 
  //print_r($record);
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://builtwith.com/target.com");
$html = str_get_html($html_content);

foreach ($html->find("div.grid_8 div") as $techdiv) {
  //print_r($tech) ;
  //foreach ($el->find("div.pT strong") as $tech){
  //  print_r($tech);
  //  print $tech->innertext . "\n";   
  //}
  //$tech = $el->find("strong"); 
  
  print $techdiv->innertext . "\n";
  //$record = array( 'tech' => $tech[4]->plaintext); 
  //print_r($record);
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://builtwith.com/target.com");
$html = str_get_html($html_content);

foreach ($html->find("div.grid_8 div") as $techdiv) {
  //print_r($tech) ;
  //foreach ($el->find("div.pT strong") as $tech){
  //  print_r($tech);
  //  print $tech->innertext . "\n";   
  //}
  //$tech = $el->find("strong"); 
  
  print $techdiv->innertext . "\n";
  //$record = array( 'tech' => $tech[4]->plaintext); 
  //print_r($record);
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://builtwith.com/target.com");
$html = str_get_html($html_content);

foreach ($html->find("div.grid_8 div") as $techdiv) {
  //print_r($tech) ;
  //foreach ($el->find("div.pT strong") as $tech){
  //  print_r($tech);
  //  print $tech->innertext . "\n";   
  //}
  //$tech = $el->find("strong"); 
  
  print $techdiv->innertext . "\n";
  //$record = array( 'tech' => $tech[4]->plaintext); 
  //print_r($record);
}
?>
