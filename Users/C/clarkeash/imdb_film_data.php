<?php

# New Scraper
$url = "http://www.imdb.com/title/tt1285016/";

$split = explode('http://www.imdb.com/title/',$url);
$split = explode('/',$split[1]);
$id = $split[0];

$html = scraperWiki::scrape($url);
           
//print $html . "\n";
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
//name and year
foreach($dom->find("h1[class='header']") as $data){
    $data2 = $data->plaintext;
    $data3 = explode('(', $data2);
    $data4 = explode(')', $data3[1]);
    $name = trim($data3[0]);
    $year = $data4[0];
}
//imdb rating
foreach($dom->find("div[class='star-box-giga-star']") as $data){
   $imdb = trim($data->plaintext);
  
}
// runtime and bbfc rating
foreach($dom->find("div[class='infobar']") as $data){
        $data2 = trim($data->plaintext);
        $data3 = explode('&nbsp;', $data2);
        $runtime = explode(' ', $data3[2]);
        $runtime = $runtime[0];
        $split = explode('"', $data);
        $bbfc = $split[5];
}
//metascore
foreach($dom->find("div[class='star-box-details']") as $data){
        $data2 = $data->plaintext;
        $split = explode('/', $data2);
        $split2 = $split[2];
        $split3 = explode('a>&nbsp; Metascore:', $split2);
        $meta = trim($split3[1]);
}
//data into array
$record = array(
        'id' => $id, 
        'name' => $name,
        'year' => $year,
        'imdb' => $imdb,
        'runtime' => $runtime,
        'bbfc' => $bbfc,
        'meta' => $meta
    );
//print_r($record);
scraperwiki::save(array('id'), $record);

?>
