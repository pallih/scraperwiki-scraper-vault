<?php

// Give ScraperWiki the page to scrape!
$html = scraperWiki::scrape("http://www.lichfieldarts.org.uk/whatson.asp");
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
    }
    else if (count($data->children) == 4) { // This is an event!
        $record = array(); // this is where our event details go
        
        $record['title'] = utf8_decode(html_entity_decode(strip_tags($data->children[2]->innertext))); // event title
        
        if (isset($data->children[2]->children[0])) { //record the link
            $record['link'] = "http://www.lichfieldarts.org.uk/".html_entity_decode(strip_tags($data->children[2]->children[0]->href));
        } else {
            $record['link'] = ""; // no link, leave blank
        }
        
        // Set the description
        $record['description'] = utf8_decode(html_entity_decode(strip_tags($data->children[2]->children[0]->innertext)));
        
        // Get the day
        $rawdate = utf8_decode(html_entity_decode(strip_tags($data->children[0]->innertext))); // from the table
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
        var_dump($record['pubDate']);
        scraperwiki::save_sqlite(array('title', 'link', 'description', 'pubDate'), $record);
        
    } else {
        echo "Not an event\n";
    }
}

?><?php

// Give ScraperWiki the page to scrape!
$html = scraperWiki::scrape("http://www.lichfieldarts.org.uk/whatson.asp");
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
    }
    else if (count($data->children) == 4) { // This is an event!
        $record = array(); // this is where our event details go
        
        $record['title'] = utf8_decode(html_entity_decode(strip_tags($data->children[2]->innertext))); // event title
        
        if (isset($data->children[2]->children[0])) { //record the link
            $record['link'] = "http://www.lichfieldarts.org.uk/".html_entity_decode(strip_tags($data->children[2]->children[0]->href));
        } else {
            $record['link'] = ""; // no link, leave blank
        }
        
        // Set the description
        $record['description'] = utf8_decode(html_entity_decode(strip_tags($data->children[2]->children[0]->innertext)));
        
        // Get the day
        $rawdate = utf8_decode(html_entity_decode(strip_tags($data->children[0]->innertext))); // from the table
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
        var_dump($record['pubDate']);
        scraperwiki::save_sqlite(array('title', 'link', 'description', 'pubDate'), $record);
        
    } else {
        echo "Not an event\n";
    }
}

?>