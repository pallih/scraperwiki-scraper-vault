<?php

require 'scraperwiki/simple_html_dom.php';  

/*scraperwiki::sqliteexecute("create table swdata (`Blocked` int, `Active` int, `New This Week` int, `DC Installs` int, `DC Downloads` int, `CK Installs` int, `CK Downloads` int, `Parsed` datetime)");
scraperwiki::sqlitecommit();*/

# User Registration Stats

$user_reg = scraperWiki::scrape("http://www.drupalcommerce.org/stats");
$dom = new simple_html_dom();
$dom->load($user_reg);
$stats = array();
foreach($dom->find("section[@id='block-views-user-total-block'] div[@class='views-row']") as $data){
    $label = false;
    $number = 0;
    foreach($data->find("div[@class='views-field-status']") as $result) {
        $label = trim($result->plaintext);
        break;
    }
    foreach($data->find("div[@class='views-field-uid']") as $result) {
        $number = $result->plaintext;
    }
    if ($label) { 
      $stats[$label] = intval(str_replace(",","",trim($number)));
    }
}
foreach($dom->find("section[@id='block-views-user-total-block-1'] div[@class='views-field-uid']") as $data){
    $stats["New This Week"] = intval(str_replace(",","",trim($data->plaintext)));
    break;
}

# Download Stats

$page = scraperWiki::scrape("http://drupal.org/project/commerce");
$dom = new simple_html_dom();
$dom->load($page);
$downloads = "";
foreach($dom->find("div[@class='project-info'] ul li") as $data){
    if (stristr($data->plaintext,"Reported")) {
        $array = explode(" ",$data->plaintext);
        $stats["DC Installs"] = intval(str_replace(",","",$array[2]));
    }
    if (stristr($data->plaintext,"Downloads")) {
        $array = explode(" ",$data->plaintext);
        $stats["DC Downloads"] = intval(str_replace(",","",$array[1]));
    }
}

$page = scraperWiki::scrape("http://drupal.org/project/commerce_kickstart");
$dom = new simple_html_dom();
$dom->load($page);
$downloads = "";
foreach($dom->find("div[@class='project-info'] ul li") as $data){
    if (stristr($data->plaintext,"Reported")) {
        $array = explode(" ",$data->plaintext);
        $stats["CK Installs"] = intval(str_replace(",","",$array[2]));
    }
    if (stristr($data->plaintext,"Downloads")) {
        $array = explode(" ",$data->plaintext);
        $stats["CK Downloads"] = intval(str_replace(",","",$array[1]));
    }
}

$stats["Parsed"] = date_create(date('Y-m-d'));
$uniquekeys = array("Parsed");
scraperwiki::save($uniquekeys,$stats);
//print_r($stats);
?>
