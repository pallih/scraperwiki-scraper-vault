<?php

// Clean up old data
scraperwiki::sqliteexecute("drop table if exists swdata"); 

// Let's build the date!
$day = date("j");
$month = date("n") - 1; // This is because January is 0 in Omnia's calendar, logical, is not it?
$year = date("Y");

// This fun fun url where is all events today \o/
$html = scraperWiki::scrape("https://www.omnia.fi/tapahtumat?p_p_id=8&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=3&_8_struts_action=%2Fcalendar%2Fview&_8_month=" .$month. "&_8_day=" .$day. "&_8_year=" .$year. "&tabs1=day");

// Install DOM
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

// Get all events
foreach($dom->find("div[class='event-title'] a") as $data){
    $text = $data->innertext; //Get event name
    $link = $data->href; //Get url to event spesific page
    print $text . "\n";
    print $link . "\n";

    // Save to ScraperWiki
    $message = scraperwiki::save_sqlite(array("text"), array("text"=>$text, "link"=>$link));           
} 

?>
