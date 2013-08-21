<?php
// WORK IN PROGRESS!! Does Not Work great just yet!

$catpages = array(
                    array('name' => 'American Restaurant',
                          'url' => 'http://www.manta.com/mb_45_C432C02T_36/american_restaurant/ohio',
                          'state' => 'Ohio',
                          'category' => 'Restaurants'));

# Blank PHP
require 'scraperwiki/simple_html_dom.php'; 
 //scraperwiki::sqliteexecute("create table if not exists manta_business_pages (`url` string)");
 //scraperwiki::sqliteexecute("create table if not exists manta_category_pages (`name` string, `url` string)");
 $states = array( 
                            array('state' => 'Alabama', 'url' => 'http://www.manta.com/mb_41_ALL_01/alabama?search=restaurants'),
                            array('state' => 'Alaska', 'url' => 'http://www.manta.com/mb_41_ALL_02/alaska?search=restaurants'),
                            array('state'=> 'Arizona', 'url' => 'http://www.manta.com/mb_41_ALL_03/arizona?search=restaurants'),
                            array('state'=> 'Arkansas', 'url' => 'http://www.manta.com/mb_41_ALL_04/arkansas?search=restaurants'),
                            array('state'=> 'California', 'url' => 'http://www.manta.com/mb_41_ALL_05/california?search=restaurants'),
                            array('state'=> 'Colorado', 'url' => 'http://www.manta.com/mb_41_ALL_06/colorado?search=restaurants'),
                            array('state'=> 'Connecticut', 'url' => 'http://www.manta.com/mb_41_ALL_07/connecticut?search=restaurants'),
                            array('state'=> 'Delaware', 'url' => 'http://www.manta.com/mb_41_ALL_08/delaware?search=restaurants'),
                            array('state'=> 'DofC', 'url' => 'http://www.manta.com/mb_41_ALL_09/district_of_columbia?search=restaurants'),
                            array('state'=> 'Florida', 'url' => 'http://www.manta.com/mb_41_ALL_10/florida?search=restaurants'),
                            array('state'=> 'Georgia', 'url' => 'http://www.manta.com/mb_41_ALL_11/georgia?search=restaurants'),
                            array('state'=> 'Hawaii', 'url' => 'http://www.manta.com/mb_41_ALL_12/hawaii?search=restaurants'),
                            array('state'=> 'Idaho', 'url' => 'http://www.manta.com/mb_41_ALL_13/idaho?search=restaurants'),
                            array('state'=> 'Illinois', 'url' => 'http://www.manta.com/mb_41_ALL_14/illinois?search=restaurants'),
                            array('state'=> 'Indiana', 'url' => 'http://www.manta.com/mb_41_ALL_15/indiana?search=restaurants'),
                            array('state'=> 'Iowa', 'url' => 'http://www.manta.com/mb_41_ALL_16/iowa?search=restaurants'),
                            array('state'=> 'Kansas', 'url' => 'http://www.manta.com/mb_41_ALL_17/kansas?search=restaurants'),
                            array('state'=> 'Kentucky', 'url' => 'http://www.manta.com/mb_41_ALL_18/kentucky?search=restaurants'),
                            array('state'=> 'Louisiana', 'url' => 'http://www.manta.com/mb_41_ALL_19/louisiana?search=restaurants'),
                            array('state'=> 'Maine', 'url' => 'http://www.manta.com/mb_41_ALL_20/maine?search=restaurants'),
                            array('state'=> 'Maryland', 'url' => 'http://www.manta.com/mb_41_ALL_21/maryland?search=restaurants'),
                            array('state'=> 'Massachussetts', 'url' => 'http://www.manta.com/mb_41_ALL_22/massachusetts?search=restaurants'),
                            array('state'=> 'Michigan', 'url' => 'http://www.manta.com/mb_41_ALL_23/michigan?search=restaurants'),
                            array('state'=> 'Minnesota', 'url' => 'http://www.manta.com/mb_41_ALL_24/minnesota?search=restaurants'),
                            array('state'=> 'Mississippi', 'url' => 'http://www.manta.com/mb_41_ALL_25/mississippi?search=restaurants'),
                            array('state'=> 'Missouri', 'url' => 'http://www.manta.com/mb_41_ALL_26/missouri?search=restaurants'),
                            array('state'=> 'Montana', 'url' => 'http://www.manta.com/mb_41_ALL_27/montana?search=restaurants'),
                            array('state'=> 'Nebraska', 'url' => 'http://www.manta.com/mb_41_ALL_28/nebraska?search=restaurants'),
                            array('state'=> 'Nevada', 'url' => 'http://www.manta.com/mb_41_ALL_29/nevada?search=restaurants'),
                            array('state'=> 'New Hampshire', 'url' => 'http://www.manta.com/mb_41_ALL_30/new_hampshire?search=restaurants'),
                            array('state'=> 'New Jersey', 'url' => 'http://www.manta.com/mb_41_ALL_31/new_jersey?search=restaurants'),
                            array('state'=> 'New Mexico', 'url' => 'http://www.manta.com/mb_41_ALL_32/new_mexico?search=restaurants'),
                            array('state'=> 'New York', 'url' => 'http://www.manta.com/mb_41_ALL_33/new_york?search=restaurants'),
                            array('state'=> 'North Carolina', 'url' => 'http://www.manta.com/mb_41_ALL_34/north_carolina?search=restaurants'),
                            array('state'=> 'North Dakota', 'url' => 'http://www.manta.com/mb_41_ALL_35/north_dakota?search=restaurants'),
                            array('state'=> 'Ohio', 'url' => 'http://www.manta.com/mb_41_ALL_36/ohio?search=restaurants'),
                            array('state'=> 'Oklahoma', 'url' => 'http://www.manta.com/mb_41_ALL_37/oklahoma?search=restaurants'),
                            array('state'=> 'Oregon', 'url' => 'http://www.manta.com/mb_41_ALL_38/oregon?search=restaurants'),
                            array('state'=> 'Pennsylvania', 'url' => 'http://www.manta.com/mb_41_ALL_39/pennsylvania?search=restaurants'),
                            array('state'=> 'Rhode Island', 'url' => 'http://www.manta.com/mb_41_ALL_40/rhode_island?search=restaurants'),
                            array('state'=> 'South Carolina', 'url' => 'http://www.manta.com/mb_41_ALL_41/south_carolina?search=restaurants'),
                            array('state'=> 'South Dakota', 'url' => 'http://www.manta.com/mb_41_ALL_42/south_dakota?search=restaurants'),
                            array('state'=> 'Tennessee', 'url' => 'http://www.manta.com/mb_41_ALL_43/tennessee?search=restaurants'),
                            array('state'=> 'Texas', 'url' => 'http://www.manta.com/mb_41_ALL_44/texas?search=restaurants'),
                            array('state'=> 'Utah', 'url' => 'http://www.manta.com/mb_41_ALL_45/utah?search=restaurants'),
                            array('state'=> 'Vermont', 'url' => 'http://www.manta.com/mb_41_ALL_46/vermont?search=restaurants'),
                            array('state'=> 'Virginia', 'url' => 'http://www.manta.com/mb_41_ALL_47/virginia?search=restaurants'),
                            array('state'=> 'Washington', 'url' => 'http://www.manta.com/mb_41_ALL_48/washington?search=restaurants'),
                            array('state'=> 'West Virginia', 'url' => 'http://www.manta.com/mb_41_ALL_49/west_virginia?search=restaurants'),
                            array('state'=> 'Wisconsin', 'url' => 'http://www.manta.com/mb_41_ALL_50/wisconsin?search=restaurants'),
                            array('state'=> 'Wyoming', 'url' => 'http://www.manta.com/mb_41_ALL_51/wyoming?search=restaurants')
                            );

 //   foreach($states as $state) {
    //$source = $state['url'];
    //Test Source http://www.manta.com/mb_41_ALL_36/ohio?pg=14&search=restaurants
    $page=20;
    $source = "http://www.manta.com/mb_41_ALL_36/ohio?search=restaurants&pg=" . $page;
    $html_content = scraperwiki::scrape("$source");
    if (isset($html_content)) { 
    $html = str_get_html($html_content);
    
    foreach ($html->find("div.address_container_info h2 a.url") as $featpage){
    echo $featpage->innertext . "\n";
    }

    foreach ($html->find("div.result-box h2 a") as $bizpage){
    echo $bizpage->innertext . "\n";
    }
} else { echo $page;}
//}




//var_dump($restaurants_by_state);
 
 //$cat_pages = array();
 
/// $pages = array();    
/// $pages[] = $source;

///$html_content = scraperwiki::scrape("$source");
///$html = str_get_html($html_content);

///foreach ($html->find("div.cols div.col ul li h4 a.mb_browse_link") as $catpage){
// $cat_pages[] = $cat->anchor;
//$cat_pages[]= array('name' => $catpage->innertext, 'url' => $catpage->href);
///echo $catpage->innertext . " - " . $catpage->href;
///print "\n";
///}

// print_r($cat_pages[0]);
/// foreach ($html->find("div.mb-main-bottom div.pagination div ul li a.mb_pagination") as $e1){
///  $pages[] = $e1->href;
///}

// var_dump($pages[0]);

/// foreach ($pages as $page){
///    $html_content = scraperwiki::scrape("$page");
///    $html = str_get_html($html_content);
///    $url = array();
///    foreach ($html->find("div.clear a") as $e2) {
///      $urls[] = $e2->href;
///      scraperwiki::sqliteexecute("insert or replace into manta_urls values (:url)", array("url"=> $e2->href));
///}
///   scraperwiki::sqlitecommit(); 
///}
 
///print_r(scraperwiki::sqliteexecute("select * from manta_urls"));
?>
