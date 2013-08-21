<?php

/** never change **/
// include external library
require 'scraperwiki/simple_html_dom.php';

// Configuration
$tablename = "Mens_Long_Jump_Final_Olympics_2012";

function getFirstMatchingElement($dom, $query) {
  $matchingElements = $dom->find($query);
  return $matchingElements[0];
}

// Get a Web page
$html_content = scraperwiki::scrape("http://london2012.bbc.co.uk/athletics/event/men-long-jump/phase=atm061100/index.html");
// Get HTML 'object'
$html = str_get_html($html_content);
/** END never change **/

/** Change the details but keep the line **/
// Create a new DB table
                                                    // `NAME OF TABLE`        `field1` type, `field2` type, etc....
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `$tablename` (`Group` text, `Rank` text, `BibNumber` text, `AthleteName` text, `Distance` text, `WindSpeed` text)");

/** Main script - needs writing each time **/

// Instantiate variables
$group = $windSpeed = $jumpers = $jumperName = $jumperRank = $bibNumber = $distance = null;

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

        $jumperRank = $col[1]->plaintext;
        $bibNumber = $col[2]->plaintext;
        $jumperName = $col[3]->plaintext;
        $distance = $col[4]->plaintext;
        $windSpeed = $col[5]->plaintext;



        

        $data = array(
            'Group' => trim($group),
            'Rank' => trim($jumperRank),
            'BibNumber' => trim($bibNumber),
            'AthleteName' => trim($jumperName),
            'Distance' => trim($distance),
            'WindSpeed' => trim($windSpeed)
        );

//        print_r($data);


        

        scraperwiki::save_sqlite(array('Group','Rank','BibNumber','AthleteName','Distance','WindSpeed'), $data, $tablename,2);

    }
}