<?php

/** never change **/
// include external library
require 'scraperwiki/simple_html_dom.php';

function getFirstMatchingElement($dom, $query) {
  $matchingElements = $dom->find($query);
  return $matchingElements[0];
}

$tablename = "US_Presidential_Election_Expenditure_Limits_by_State";

// Get a Web page
$html_content = scraperwiki::scrape("http://www.fec.gov/pages/brochures/pubfund_limits_2012.shtml");
// Get HTML 'object'
$html = str_get_html($html_content);
/** END never change **/

/** Change the details but keep the line **/
// Create a new DB table
                                                    /* `NAME OF TABLE`        `field1` type, `field2` type, etc.... */
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `US_Presidential_Election_Expenditure_Limits_by_State` (`State` text, `VotingAgePopulation` text, `Limit` text)"); 

/** Main script - needs writing each time **/

// Instantiate variables
$limits = $limitsDom = null;


// DOM search
$limitTable = $html->find("table");



foreach ($limitTable as $limitsTableNode) {


      $limits = $limitsTableNode->firstChild()->children() ;



            foreach ($limits as $state ) {

            $col = $state->find("td") ;



            $stateName = $col[0]->plaintext;
            $votingAgePopulation = $col[1]->plaintext;
            $expenditureLimitation = $col[2]->plaintext;

            
            $data = array(
            'State' => trim($stateName),
            'VotingAgePopulation' => trim($votingAgePopulation),
            'Limit' => trim($expenditureLimitation)
            );
        }

        scraperwiki::save_sqlite(array('State','VotingAgePopulation','Limit'), $data, $tablename,2);


}


?>
<?php

/** never change **/
// include external library
require 'scraperwiki/simple_html_dom.php';

function getFirstMatchingElement($dom, $query) {
  $matchingElements = $dom->find($query);
  return $matchingElements[0];
}

$tablename = "US_Presidential_Election_Expenditure_Limits_by_State";

// Get a Web page
$html_content = scraperwiki::scrape("http://www.fec.gov/pages/brochures/pubfund_limits_2012.shtml");
// Get HTML 'object'
$html = str_get_html($html_content);
/** END never change **/

/** Change the details but keep the line **/
// Create a new DB table
                                                    /* `NAME OF TABLE`        `field1` type, `field2` type, etc.... */
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `US_Presidential_Election_Expenditure_Limits_by_State` (`State` text, `VotingAgePopulation` text, `Limit` text)"); 

/** Main script - needs writing each time **/

// Instantiate variables
$limits = $limitsDom = null;


// DOM search
$limitTable = $html->find("table");



foreach ($limitTable as $limitsTableNode) {


      $limits = $limitsTableNode->firstChild()->children() ;



            foreach ($limits as $state ) {

            $col = $state->find("td") ;



            $stateName = $col[0]->plaintext;
            $votingAgePopulation = $col[1]->plaintext;
            $expenditureLimitation = $col[2]->plaintext;

            
            $data = array(
            'State' => trim($stateName),
            'VotingAgePopulation' => trim($votingAgePopulation),
            'Limit' => trim($expenditureLimitation)
            );
        }

        scraperwiki::save_sqlite(array('State','VotingAgePopulation','Limit'), $data, $tablename,2);


}


?>
