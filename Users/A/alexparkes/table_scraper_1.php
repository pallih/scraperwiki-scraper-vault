<?php

/** never change **/
// include external library
require 'scraperwiki/simple_html_dom.php';

function getFirstMatchingElement($dom, $query) {
  $matchingElements = $dom->find($query);
  return $matchingElements[0];
}

// Get a Web page
$html_content = scraperwiki::scrape("http://london2012.bbc.co.uk/athletics/event/men-200m/phase=atm002900/index.html");
// Get HTML 'object'
$html = str_get_html($html_content);
/** END never change **/

/** Change the details but keep the line **/
// Create a new DB table
                                                    // `NAME OF TABLE`        `field1` type, `field2` type, etc....
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `Mens_200m_Round1_Olympics_2012` (`Heat` text, `WindSpeed` text, `Rank` text, `BibNumber` text, `AthleteName` text, `Time` text, `QualifiedForNextRount` text, `PersonalBest` text, `ReactionTime` text)");

/** Main script - needs writing each time **/

// Instantiate variables
$heat = $windSpeed = $runners = $runnerName = $runnerRank = $bibNumber = $time = $qualified = $personalBest = null;

// DOM search
$heats = $html->find("div.or-unitHeader");
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

// loop over results (create a var called "heatDiv")
foreach ($heats as $heatHeaderDiv) {

    $heat = getFirstMatchingElement($heatHeaderDiv, "div.or-unit")->plaintext; // get all text from DOM object
    $windSpeed = getFirstMatchingElement($heatHeaderDiv, "div.or-wind")->plaintext;
    $windSpeed = substr($windSpeed, 20);

    $runnerRows = $heatHeaderDiv->nextSibling()->find("table > tbody > tr[class]");

/**
$tableElement = $roundHeader->nextSibling();
$matches = $tableElement->find(whatever);
**/
    
    foreach ($runnerRows as $index => $runner) {
        if (($index & 1) == 0) {

            $col = $runner->find("td"); // actually CELL
            if (count($col) == 0) { // if no CELLS
                continue; // then skip row
            }

            $runnerName = $col[3]->plaintext;
            $runnerRank = $col[1]->plaintext;
            $bibNumber = $col[2]->plaintext;
            $time = $col[4]->plaintext;
            $qualified = $col[5]->plaintext;

            if ($qualified == "q" || $qualified == "Q") {
                $qualified = "true";
            } else {
                $qualified = "false";
            }

            if (count($col) < 7 || $col[6]->plaintext == "") {
                $personalBest = " ";
            } else {
                $personalBest = $col[6]->plaintext;
            }

            $reactionTimeSpan = $runner->nextSibling()->find("span.or-value");
            $reactionTime = $reactionTimeSpan[0]->plaintext;
    
            // Create data array
            $data = array( // comma delimited
                'Heat' => $heat,
                'WindSpeed' => $windSpeed,
                'Rank' => $runnerRank,
                'BibNumber' => $bibNumber,
                'AthleteName' => $runnerName,
                'Time' => $time,
                'QualifiedForNextRount' => $qualified,
                'PersonalBest' => $personalBest,
                'ReactionTime' => $reactionTime
            );    

            // add data array to table
            scraperwiki::save_sqlite(array('Heat', 'WindSpeed', 'Rank', 'BibNumber', 'AthleteName', 'Time', 'QualifiedForNextRount', 'PersonalBest', 'ReactionTime'), $data, "Mens_200m_Round1_Olympics_2012", 2);

        }
    
        
    }
}<?php

/** never change **/
// include external library
require 'scraperwiki/simple_html_dom.php';

function getFirstMatchingElement($dom, $query) {
  $matchingElements = $dom->find($query);
  return $matchingElements[0];
}

// Get a Web page
$html_content = scraperwiki::scrape("http://london2012.bbc.co.uk/athletics/event/men-200m/phase=atm002900/index.html");
// Get HTML 'object'
$html = str_get_html($html_content);
/** END never change **/

/** Change the details but keep the line **/
// Create a new DB table
                                                    // `NAME OF TABLE`        `field1` type, `field2` type, etc....
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `Mens_200m_Round1_Olympics_2012` (`Heat` text, `WindSpeed` text, `Rank` text, `BibNumber` text, `AthleteName` text, `Time` text, `QualifiedForNextRount` text, `PersonalBest` text, `ReactionTime` text)");

/** Main script - needs writing each time **/

// Instantiate variables
$heat = $windSpeed = $runners = $runnerName = $runnerRank = $bibNumber = $time = $qualified = $personalBest = null;

// DOM search
$heats = $html->find("div.or-unitHeader");
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

// loop over results (create a var called "heatDiv")
foreach ($heats as $heatHeaderDiv) {

    $heat = getFirstMatchingElement($heatHeaderDiv, "div.or-unit")->plaintext; // get all text from DOM object
    $windSpeed = getFirstMatchingElement($heatHeaderDiv, "div.or-wind")->plaintext;
    $windSpeed = substr($windSpeed, 20);

    $runnerRows = $heatHeaderDiv->nextSibling()->find("table > tbody > tr[class]");

/**
$tableElement = $roundHeader->nextSibling();
$matches = $tableElement->find(whatever);
**/
    
    foreach ($runnerRows as $index => $runner) {
        if (($index & 1) == 0) {

            $col = $runner->find("td"); // actually CELL
            if (count($col) == 0) { // if no CELLS
                continue; // then skip row
            }

            $runnerName = $col[3]->plaintext;
            $runnerRank = $col[1]->plaintext;
            $bibNumber = $col[2]->plaintext;
            $time = $col[4]->plaintext;
            $qualified = $col[5]->plaintext;

            if ($qualified == "q" || $qualified == "Q") {
                $qualified = "true";
            } else {
                $qualified = "false";
            }

            if (count($col) < 7 || $col[6]->plaintext == "") {
                $personalBest = " ";
            } else {
                $personalBest = $col[6]->plaintext;
            }

            $reactionTimeSpan = $runner->nextSibling()->find("span.or-value");
            $reactionTime = $reactionTimeSpan[0]->plaintext;
    
            // Create data array
            $data = array( // comma delimited
                'Heat' => $heat,
                'WindSpeed' => $windSpeed,
                'Rank' => $runnerRank,
                'BibNumber' => $bibNumber,
                'AthleteName' => $runnerName,
                'Time' => $time,
                'QualifiedForNextRount' => $qualified,
                'PersonalBest' => $personalBest,
                'ReactionTime' => $reactionTime
            );    

            // add data array to table
            scraperwiki::save_sqlite(array('Heat', 'WindSpeed', 'Rank', 'BibNumber', 'AthleteName', 'Time', 'QualifiedForNextRount', 'PersonalBest', 'ReactionTime'), $data, "Mens_200m_Round1_Olympics_2012", 2);

        }
    
        
    }
}