<?php
$html = scraperWiki::scrape("http://filmguide.sundance.org/filmguide/event/all_films");
//print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.base td.ofg_table") as $data){
   $tds = $data->find("a");
   $tds2 = $data->find("p");
   $tds3 = $data->find("a img.still_image_grid");
    $record = array(
        'film_title' => $tds[1]->plaintext, 
        'film_summary' => $tds2[0]->plaintext,
        'film_image' => $tds3[0]->src);
//$record[] = array("title"=>$title, "description"=>$description, "image"=>$image);
//print_r($record);
scraperwiki::save(array('film_title'), $record);
}
?>
<?php
$html = scraperWiki::scrape("http://filmguide.sundance.org/filmguide/event/all_films");
//print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.base td.ofg_table") as $data){
   $tds = $data->find("a");
   $tds2 = $data->find("p");
   $tds3 = $data->find("a img.still_image_grid");
    $record = array(
        'film_title' => $tds[1]->plaintext, 
        'film_summary' => $tds2[0]->plaintext,
        'film_image' => $tds3[0]->src);
//$record[] = array("title"=>$title, "description"=>$description, "image"=>$image);
//print_r($record);
scraperwiki::save(array('film_title'), $record);
}
?>
