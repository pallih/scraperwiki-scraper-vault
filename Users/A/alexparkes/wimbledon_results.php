<?php

/** never change **/
// include external library
require 'scraperwiki/simple_html_dom.php';

// Get a Web page
$html_content = scraperwiki::scrape("http://news.bbc.co.uk/sport1/hi/tennis/results/default.stm");
// Get HTML 'object'
$html = str_get_html($html_content);
/** END never change **/

/** Change the details but keep the line **/
// Create a new DB table
                                                    // `NAME OF TABLE`        `field1` type, `field2` type, etc....
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `wimbledon_2012_data` (`winner` text, `looser` text, `round` text)");

/** Main script - needs writing each time **/

// Instantiate variables
$winner = $looser = $round = null;

// DOM search
$rounds = $html->find("div.datasection h3");
// find("tag") // == find all tags of type "tag", eg <tag>
// find("#id") // == find the tag with id "id", eg <tag id="id">
// find(".class") // == find all tags with "class" class, eg <tag class="class">
// find("ancestor relative") // find all "relative" tags which exist under an "ancestor" tag, eg <ancestor><tag><relative></relative></tag></ancestor>
// find("parent > child") // as above but only with first direct level children, eg <ancestor><relative></relative></ancestor>
// example of combo:
// find("div#data li.visible") // select all the "li" tags with class "visible" under a div with id "data"

/**
foreach ($registerOfChildren as $childName) {
    // run this code
    echo "Are you here, " . $childName . "?";
}
**/

// loop over results (create a var called "roundHeader")
foreach ($rounds as $roundHeader) {
    $round = $roundHeader->innertext; // get all text from DOM object
    $matches = $roundHeader->nextSibling()->find("tr"); // DOM traverse

/**
$tableElement = $roundHeader->nextSibling();
$matches = $tableElement->find(whatever);
**/
    
    foreach ($matches as $match) {
        $row = str_get_html($match);
        $col = $row->find("td"); // actually CELL
        if (count($col) == 0) { // if no CELLS
            continue; // then skip row
        }
    
        $winner = $col[0]->innertext;
        $looser = $col[4]->innertext;

        if (!$winner || !$looser)
            continue;
    
        // Create data array
        $data = array( // comma delimited
            'winner' => $winner,
            'looser' => $looser,
            'round' => $round
        );    
    
        // add data array to table
                                    //('fieldname1', 'fieldname2'),  $data, "table name", ???);
        scraperwiki::save_sqlite(array('winner', 'looser', 'round'), $data, "wimbledon_2012_data", 2);
    }
}<?php

/** never change **/
// include external library
require 'scraperwiki/simple_html_dom.php';

// Get a Web page
$html_content = scraperwiki::scrape("http://news.bbc.co.uk/sport1/hi/tennis/results/default.stm");
// Get HTML 'object'
$html = str_get_html($html_content);
/** END never change **/

/** Change the details but keep the line **/
// Create a new DB table
                                                    // `NAME OF TABLE`        `field1` type, `field2` type, etc....
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `wimbledon_2012_data` (`winner` text, `looser` text, `round` text)");

/** Main script - needs writing each time **/

// Instantiate variables
$winner = $looser = $round = null;

// DOM search
$rounds = $html->find("div.datasection h3");
// find("tag") // == find all tags of type "tag", eg <tag>
// find("#id") // == find the tag with id "id", eg <tag id="id">
// find(".class") // == find all tags with "class" class, eg <tag class="class">
// find("ancestor relative") // find all "relative" tags which exist under an "ancestor" tag, eg <ancestor><tag><relative></relative></tag></ancestor>
// find("parent > child") // as above but only with first direct level children, eg <ancestor><relative></relative></ancestor>
// example of combo:
// find("div#data li.visible") // select all the "li" tags with class "visible" under a div with id "data"

/**
foreach ($registerOfChildren as $childName) {
    // run this code
    echo "Are you here, " . $childName . "?";
}
**/

// loop over results (create a var called "roundHeader")
foreach ($rounds as $roundHeader) {
    $round = $roundHeader->innertext; // get all text from DOM object
    $matches = $roundHeader->nextSibling()->find("tr"); // DOM traverse

/**
$tableElement = $roundHeader->nextSibling();
$matches = $tableElement->find(whatever);
**/
    
    foreach ($matches as $match) {
        $row = str_get_html($match);
        $col = $row->find("td"); // actually CELL
        if (count($col) == 0) { // if no CELLS
            continue; // then skip row
        }
    
        $winner = $col[0]->innertext;
        $looser = $col[4]->innertext;

        if (!$winner || !$looser)
            continue;
    
        // Create data array
        $data = array( // comma delimited
            'winner' => $winner,
            'looser' => $looser,
            'round' => $round
        );    
    
        // add data array to table
                                    //('fieldname1', 'fieldname2'),  $data, "table name", ???);
        scraperwiki::save_sqlite(array('winner', 'looser', 'round'), $data, "wimbledon_2012_data", 2);
    }
}