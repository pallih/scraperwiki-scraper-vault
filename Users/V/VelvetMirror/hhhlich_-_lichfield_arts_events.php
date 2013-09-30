<?php
// Give ScraperWiki the page to scrape!
$base_url = "http://www.lichfieldarts.org.uk/whatson.asp";
$html = scraperWiki::scrape($base_url);
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

// Build an array of months for.... errrm....
$months = array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");

// Find all the rows in the main events table
foreach($dom->find("table[@cellpadding='4']/tr") as $data) {
    
    // Only one child element so must be a header row to indicate the month
    if (count($data->children) == 1){
        // Set the current month of all the events we're about to scrape
        $this_month = strip_tags($data->children[0]->innertext);
        // Gives us $splitmonth['month'] and $splitmonth['year']
        preg_match("/(?<month>\w+)(\s|&nbsp;|$)(?<year>\d+)/", $this_month, $splitmonth);
        //print $splitmonth['month'] | $splitmonth['year'] . "\n";
    }
    else if(count($data->children == 4)) { // This represents an event.
        $record = array(); // Event details will be saved here

        $record['title'] = $data->children(2)->children(0)->plaintext; // Sets the title.

        $link = $data->children(2)->children(0)->href . "\n";

        if (isset($link)) {
            $record['link'] = $base_url . $link; // Sets the link. 
        }
        else {
            $record['link'] = ''; // If there is no link, leave blank.
        }        

        // Set the description
        $record['description'] = utf8_decode(html_entity_decode(strip_tags($data->children[2]->children[0]->innertext)));

        // Get the day
        $rawdate = trim($data->children(0)->plaintext) . "\n";
        preg_match("/(?<day>\w+) (?<day_num>\d+)(?<day_suffix>\w{2})(\(\w+\))?/", $rawdate, $splitdate); // date now in $splitdate['day_num']

        // get the time
        $rawtime = utf8_decode(html_entity_decode(strip_tags($data->children[1]->innertext)));
        if (strpos($rawtime, "TBC") !== false){ $splittime = array('hours'=>0, 'mins'=>0, 'time_of_day'=>'am'); } //TBC so set to midnight
        else if (strpos($rawtime, "Noon") !== false || empty($rawtime)){ //"Noon" or empty
            $splittime = array('hours'=>12, 'mins'=>0, 'time_of_day'=>'pm');
        }
        else {preg_match("/(?<hours>\d+)((:|\.)(?<mins>\d+))?(?<time_of_day>\w+)/", $rawtime, $splittime);} //split the time

        // Assemble the full date and time
        $build_date = $splitdate['day_num'].' '.$splitmonth['month'].' '.$splitmonth['year'].' ';
        $build_date .= $splittime['hours'].':'.$splittime['mins'].$splittime['time_of_day'];
        $record['pubDate'] = date('Y-m-d H:i:s', strtotime($build_date)); // convert to ISO 8601 for SQLlite
        scraperwiki::save(array('title', 'link', 'description', 'pubDate'), $record);
     }
}<?php
// Give ScraperWiki the page to scrape!
$base_url = "http://www.lichfieldarts.org.uk/whatson.asp";
$html = scraperWiki::scrape($base_url);
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

// Build an array of months for.... errrm....
$months = array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");

// Find all the rows in the main events table
foreach($dom->find("table[@cellpadding='4']/tr") as $data) {
    
    // Only one child element so must be a header row to indicate the month
    if (count($data->children) == 1){
        // Set the current month of all the events we're about to scrape
        $this_month = strip_tags($data->children[0]->innertext);
        // Gives us $splitmonth['month'] and $splitmonth['year']
        preg_match("/(?<month>\w+)(\s|&nbsp;|$)(?<year>\d+)/", $this_month, $splitmonth);
        //print $splitmonth['month'] | $splitmonth['year'] . "\n";
    }
    else if(count($data->children == 4)) { // This represents an event.
        $record = array(); // Event details will be saved here

        $record['title'] = $data->children(2)->children(0)->plaintext; // Sets the title.

        $link = $data->children(2)->children(0)->href . "\n";

        if (isset($link)) {
            $record['link'] = $base_url . $link; // Sets the link. 
        }
        else {
            $record['link'] = ''; // If there is no link, leave blank.
        }        

        // Set the description
        $record['description'] = utf8_decode(html_entity_decode(strip_tags($data->children[2]->children[0]->innertext)));

        // Get the day
        $rawdate = trim($data->children(0)->plaintext) . "\n";
        preg_match("/(?<day>\w+) (?<day_num>\d+)(?<day_suffix>\w{2})(\(\w+\))?/", $rawdate, $splitdate); // date now in $splitdate['day_num']

        // get the time
        $rawtime = utf8_decode(html_entity_decode(strip_tags($data->children[1]->innertext)));
        if (strpos($rawtime, "TBC") !== false){ $splittime = array('hours'=>0, 'mins'=>0, 'time_of_day'=>'am'); } //TBC so set to midnight
        else if (strpos($rawtime, "Noon") !== false || empty($rawtime)){ //"Noon" or empty
            $splittime = array('hours'=>12, 'mins'=>0, 'time_of_day'=>'pm');
        }
        else {preg_match("/(?<hours>\d+)((:|\.)(?<mins>\d+))?(?<time_of_day>\w+)/", $rawtime, $splittime);} //split the time

        // Assemble the full date and time
        $build_date = $splitdate['day_num'].' '.$splitmonth['month'].' '.$splitmonth['year'].' ';
        $build_date .= $splittime['hours'].':'.$splittime['mins'].$splittime['time_of_day'];
        $record['pubDate'] = date('Y-m-d H:i:s', strtotime($build_date)); // convert to ISO 8601 for SQLlite
        scraperwiki::save(array('title', 'link', 'description', 'pubDate'), $record);
     }
}