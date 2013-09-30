<?php
$html = scraperWiki::scrape("http://filmguide.sundance.org/film/120061/_revolution");
//print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.base") as $data){
   $tds = $data->find("div");
   $tds2 = $data->find("p");
   $tds3 = $data->find("div#tabs p");
   $tds4 = $data->find("table img");
   $tds5 = $data->find("p strong");
   $tds6 = $data->find("p a");
   $tds7 = $data->find("p.byline");
    $record = array(
        'film_title' => $tds[3]->plaintext, 
        'film_summary' => $tds3[0]->plaintext,
        'film_image' => $tds4[0]->src,
        'film_description' => $tds2[0]->plaintext,
        'film_director' => $tds5[0]->plaintext,
        'film_category' => $tds6[0]->plaintext,
        'film_byline' => $tds7[0]->plaintext);
//$record[] = array("title"=>$title, "description"=>$description, "image"=>$image);
//print_r($record);
scraperwiki::save(array('film_title'), $record);
}
?>
<?php
$html = scraperWiki::scrape("http://filmguide.sundance.org/film/120061/_revolution");
//print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.base") as $data){
   $tds = $data->find("div");
   $tds2 = $data->find("p");
   $tds3 = $data->find("div#tabs p");
   $tds4 = $data->find("table img");
   $tds5 = $data->find("p strong");
   $tds6 = $data->find("p a");
   $tds7 = $data->find("p.byline");
    $record = array(
        'film_title' => $tds[3]->plaintext, 
        'film_summary' => $tds3[0]->plaintext,
        'film_image' => $tds4[0]->src,
        'film_description' => $tds2[0]->plaintext,
        'film_director' => $tds5[0]->plaintext,
        'film_category' => $tds6[0]->plaintext,
        'film_byline' => $tds7[0]->plaintext);
//$record[] = array("title"=>$title, "description"=>$description, "image"=>$image);
//print_r($record);
scraperwiki::save(array('film_title'), $record);
}
?>
