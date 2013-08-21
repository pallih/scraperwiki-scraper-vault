<?php

$asdaURLPrefix = 'http://direct.asda.com/on/demandware.store/Sites-ASDA-Site/default/Search-Show?q=';

require 'scraperwiki/simple_html_dom.php'; 

$data = scraperWiki::scrape('http://leapgradient.com/asda/Test_File_for_Amazon_Scrap.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $url= $row[2];
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
        foreach ($html->find("div.relatedSearches a") as $el) {
            $asdaURL = $asdaURLPrefix . str_replace(" ", "+", $el->innertext);
            $asda_html_content = scraperwiki::scrape($asdaURL);
            $asda_html = str_get_html($asda_html_content);
            foreach ($asda_html->find("div.showing") as $asdaResultSet) {
                $resultCountText = $asdaResultSet->plaintext;
                preg_match('/ of [0-9\.\-]*/', $resultCountText, $matches);
                $resultCount = str_replace(" of ", "", $matches[0]) . "\n";
                $record = array(
                    'searchTerm' => str_replace("+"," ",$row[1]) . " - " . $el->plaintext, 
                    'relatedTerms' => str_replace("."," ",str_replace("Related Searches: "," ",$el->plaintext)),
                    'resultsFoundOnAsdaDirect' => 'true',
                    'noOfResultsFoundOnAsdaDirect' => $resultCount
                );
                scraperwiki::save(array('searchTerm'), $record); 
                break;
            }
        }
       foreach ($html->find("div.didYouMean") as $el) {
         //  print $el->plaintext . "\n";
           $asdaURL = $asdaURLPrefix . str_replace(" ", "+", trim(str_replace("Did you mean: ","",$el->plaintext)));
//print $asdaURL . "\n";
           $asda_html_content = scraperwiki::scrape($asdaURL);
           $asda_html = str_get_html($asda_html_content);
           foreach ($asda_html->find("div.showing") as $asdaResultSet) {
               $resultCountText = $asdaResultSet->plaintext;
               preg_match('/ of [0-9\.\-]*/', $resultCountText, $matches);
               $resultCount = str_replace(" of ", "", $matches[0]) . "\n";
               $record = array(
                    'searchTerm' => str_replace("+"," ",$row[1]) . "-" . trim(str_replace("Did you mean: ","",$el->plaintext)), 
                    'didYouMean' => str_replace("Did you mean: "," ",$el->plaintext),
                    'resultsFoundOnAsdaDirect' => 'true',
                    'noOfResultsFoundOnAsdaDirect' => $resultCount
                );
          //  print json_encode($record) . "\n";
            scraperwiki::save(array('searchTerm'), $record);
             }
       }
}



?>
