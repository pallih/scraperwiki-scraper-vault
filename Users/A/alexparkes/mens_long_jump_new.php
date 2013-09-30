<?php

/** never change **/
// include external library
require 'scraperwiki/simple_html_dom.php';

function getFirstMatchingElement($dom, $query) {
  $matchingElements = $dom->find($query);
  return $matchingElements[0];
}

// Get a Web page
$html_content = scraperwiki::scrape("http://london2012.bbc.co.uk/athletics/event/men-long-jump/phase=atm061900/index.html");
// Get HTML 'object'
$html = str_get_html($html_content);
/** END never change **/

/** Change the details but keep the line **/
// Create a new DB table
                                                    /* `NAME OF TABLE`        `field1` type, `field2` type, etc....
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `Mens_Long_Jump_Qualifying_Olympics_2012` (`Group` text, `Rank` text, `BibNumber` text, `AthleteName` text, `Distance` text, `QualifiedForNextRount` text, `PersonalBest` text, `WindSpeed` text)"); */

/** Main script - needs writing each time **/

// Instantiate variables
$group = $windSpeed = $jumpers = $jumperName = $jumperRank = $bibNumber = $distance = $qualified = $personalBest = null;

// DOM search
$groups = $html->find("div.or-unitHeader");


foreach ($groups as $groupHeaderNode) {

    $groupDom = str_get_html($groupHeaderNode);
    
    $group = $groupDom->find("div.or-unit") ;
    $group = $group[0]->plaintext ; 

    $jumperRows = $groupHeaderNode->nextSibling()->children(1)->children() ;
    
    foreach ($jumperRows as $count => $jumper) {

        $col = $jumper->find("td") ;
        if (count($col) == 0 || preg_match("/or-hide/", $jumper->class) == 1) {
            continue;
        }



        if ($group == "Group A") {

        $jumperRank = $col[1]->plaintext;
        $bibNumber = $col[2]->plaintext;
        $jumperName = $col[3]->plaintext;
        $distance = $col[4]->plaintext;
        $qualified = $col[5]->plaintext;
   
        if ($qualified == "Q") {$qualified = "Qualified by position";}
        elseif ($qualified == "q") {$qualified = "Qualified by distance";}
        else {$qualified = "Did not qualify";}

        if ($col[6]->plaintext == " ") {$personalBest = "Not personal, season or national best";}
        else {$personalBest = $col[6]->plaintext;}

        $windSpeed = $col[7]->plaintext;
        

    $data = array(
        'Group' => $group,
        'Rank' => $jumperRank,
        'BibNumber' => $bibNumber,
        'AthleteName' => $jumperName,
        'Distance' => $distance,
        'QualifiedForNextRount' => $qualified,
        'PersonalBest' => $personalBest,
        'WindSpeed' => $windSpeed
            );

            scraperwiki::save_sqlite(array('Group', 'Rank', 'BibNumber', 'AthleteName', 'Distance', 'QualifiedForNextRount', 'PersonalBest', 'WindSpeed'), $data, "Mens_Long_Jump_Qualifying_GroupA_Olympics_2012", 2);
        }

        else {

        $jumperRank = $col[1]->plaintext;
        $bibNumber = $col[2]->plaintext;
        $jumperName = $col[3]->plaintext;
        $distance = $col[4]->plaintext;
        $qualified = $col[5]->plaintext;

            if ($qualified == "Q") {$qualified = "Qualified by position";}
            elseif ($qualified == "q") {$qualified = "Qualified by distance";}
            else {$qualified = "Did not qualify";}

        $windSpeed = $col[6]->plaintext;
        

    $data = array(
        'Group' => $group,
        'Rank' => $jumperRank,
        'BibNumber' => $bibNumber,
        'AthleteName' => $jumperName,
        'Distance' => $distance,
        'QualifiedForNextRount' => $qualified,
        'WindSpeed' => $windSpeed
            );

            scraperwiki::save_sqlite(array('Group', 'Rank', 'BibNumber', 'AthleteName', 'Distance', 'QualifiedForNextRount', 'WindSpeed'), $data, "Mens_Long_Jump_Qualifying_GroupB_Olympics_2012", 2);
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
$html_content = scraperwiki::scrape("http://london2012.bbc.co.uk/athletics/event/men-long-jump/phase=atm061900/index.html");
// Get HTML 'object'
$html = str_get_html($html_content);
/** END never change **/

/** Change the details but keep the line **/
// Create a new DB table
                                                    /* `NAME OF TABLE`        `field1` type, `field2` type, etc....
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `Mens_Long_Jump_Qualifying_Olympics_2012` (`Group` text, `Rank` text, `BibNumber` text, `AthleteName` text, `Distance` text, `QualifiedForNextRount` text, `PersonalBest` text, `WindSpeed` text)"); */

/** Main script - needs writing each time **/

// Instantiate variables
$group = $windSpeed = $jumpers = $jumperName = $jumperRank = $bibNumber = $distance = $qualified = $personalBest = null;

// DOM search
$groups = $html->find("div.or-unitHeader");


foreach ($groups as $groupHeaderNode) {

    $groupDom = str_get_html($groupHeaderNode);
    
    $group = $groupDom->find("div.or-unit") ;
    $group = $group[0]->plaintext ; 

    $jumperRows = $groupHeaderNode->nextSibling()->children(1)->children() ;
    
    foreach ($jumperRows as $count => $jumper) {

        $col = $jumper->find("td") ;
        if (count($col) == 0 || preg_match("/or-hide/", $jumper->class) == 1) {
            continue;
        }



        if ($group == "Group A") {

        $jumperRank = $col[1]->plaintext;
        $bibNumber = $col[2]->plaintext;
        $jumperName = $col[3]->plaintext;
        $distance = $col[4]->plaintext;
        $qualified = $col[5]->plaintext;
   
        if ($qualified == "Q") {$qualified = "Qualified by position";}
        elseif ($qualified == "q") {$qualified = "Qualified by distance";}
        else {$qualified = "Did not qualify";}

        if ($col[6]->plaintext == " ") {$personalBest = "Not personal, season or national best";}
        else {$personalBest = $col[6]->plaintext;}

        $windSpeed = $col[7]->plaintext;
        

    $data = array(
        'Group' => $group,
        'Rank' => $jumperRank,
        'BibNumber' => $bibNumber,
        'AthleteName' => $jumperName,
        'Distance' => $distance,
        'QualifiedForNextRount' => $qualified,
        'PersonalBest' => $personalBest,
        'WindSpeed' => $windSpeed
            );

            scraperwiki::save_sqlite(array('Group', 'Rank', 'BibNumber', 'AthleteName', 'Distance', 'QualifiedForNextRount', 'PersonalBest', 'WindSpeed'), $data, "Mens_Long_Jump_Qualifying_GroupA_Olympics_2012", 2);
        }

        else {

        $jumperRank = $col[1]->plaintext;
        $bibNumber = $col[2]->plaintext;
        $jumperName = $col[3]->plaintext;
        $distance = $col[4]->plaintext;
        $qualified = $col[5]->plaintext;

            if ($qualified == "Q") {$qualified = "Qualified by position";}
            elseif ($qualified == "q") {$qualified = "Qualified by distance";}
            else {$qualified = "Did not qualify";}

        $windSpeed = $col[6]->plaintext;
        

    $data = array(
        'Group' => $group,
        'Rank' => $jumperRank,
        'BibNumber' => $bibNumber,
        'AthleteName' => $jumperName,
        'Distance' => $distance,
        'QualifiedForNextRount' => $qualified,
        'WindSpeed' => $windSpeed
            );

            scraperwiki::save_sqlite(array('Group', 'Rank', 'BibNumber', 'AthleteName', 'Distance', 'QualifiedForNextRount', 'WindSpeed'), $data, "Mens_Long_Jump_Qualifying_GroupB_Olympics_2012", 2);
        }
       
    }
}