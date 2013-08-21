<?php

scraperwiki::sqliteexecute("drop table if exists swdata");

require 'scraperwiki/simple_html_dom.php';
$stateCode["VIC"] = 1;
$stateCode["NSW"] = 2;
$stateCode["QLD"] = 3;
$stateCode["SA"] = 4;
$stateCode["TAS"] = 5;
// no idea why WA data is not available.

function fetchPage($stateCode) {
  // fetch the page and return a string of the whole page.

  // construct the targetURL in the format
  // http://indicator.theclimategroup.org/results/this_week?state_id=X


  $srcURL = "http://indicator.theclimategroup.org/results/this_week";
  $parameterName = "state_id";
  $paramVal = $stateCode;
  $targetURL = $srcURL . "?" . $parameterName . "=" . $paramVal;
  
  // fetch the page from the targetURL
  $html_content = scraperwiki::scrape($targetURL);
  $html = str_get_html($html_content);
  return $html;

}

function parsePage_thisYearToDate($str) {
// $str is a strong representing an HTML document
// returns a string representing the year to date C02E emissions (in millions of tonnes) 


 // extract the first <p> tag in the document
 $HTMLChunk = $str->find('p', 0);
  
// $HTMLChunk is expected to be in the following format
//
# START
# <p>
# <strong>This year to date:</strong> 47.807 million tonnes CO<sub style="font-size: 60%;">2</sub>
#</p>
# END
$pattern = "/([0-9]+)\.?([0-9]?)/i";
$subject = $HTMLChunk;

if (preg_match($pattern, $subject, $matches)) {
    #echo "A match was found.";
    #print "\n" . $matches[0] . "\n";
    return $matches[0];
}
 
}


function parsePage_thisWeek($str) {
// $str is a strong representing an HTML document
// returns a string representing the C02E emissions (in millions of tonnes) for this week


 // extract the first <h3> tag in the document
 $HTMLChunk = $str->find('h3', 0);
  //print $HTMLChunk;
// $HTMLChunk is expected to be in the following format
//
# START
#<h3>
#2.183 million tonnes CO
#<sub style="font-size: 60%;">2</sub>
#e
#</h3>
# END
 $pattern = "/<h3\b[^>]*>([0-9]+)\.?([0-9]?)/i";
#$pattern = "/(<h3\b[^>]*)>/i";
$subject = $HTMLChunk;

if (preg_match($pattern, $subject, $matches)) {
    echo "A match was found.";
    print "\n" . $matches[0] . "\n";
    return $matches[0];
}
 
}


function saveIt($c02E_YTD, $c02E_thisWeek,$state) {
// save the record in the db

$record = array('year'=>date('Y'),'state'=>$state,'week'=>date('W'),'date'=>date('j/m/Y'),'c02E_this_week'=>$c02E_thisWeek,'c02E_year_to_date' => $c02E_YTD);
scraperwiki::save(array('state','week'), $record);  

}

foreach ($stateCode as $key => $value) {   
// fetch page
$page = fetchPage($value);

// get tonnes of carbon this year to date
$carbontonnes_ytd = parsePage_thisYearToDate($page);
$carbontonnes_thisWeek = parsePage_thisWeek($page);

// save the data
saveIt($carbontonnes_ytd, $carbontonnes_thisWeek,$key);
}

?>
