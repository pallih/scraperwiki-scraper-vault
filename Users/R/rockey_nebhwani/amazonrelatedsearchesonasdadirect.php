<?php

$asdaURLPrefix = 'http://direct.asda.com/on/demandware.store/Sites-ASDA-Site/default/Search-Show?q=';

require 'scraperwiki/simple_html_dom.php'; 

// CSV format - SLEGDE,SLEGDE,http://www.amazon.co.uk/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=SLEGDE,Product Type,SLEGDE,32.0

$data = scraperWiki::scrape('http://leapgradient.com/asda/ASDA_Search_Insights_Report_W20130221.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $url= $row[2];

//First of all check that term being reported is still returning null page or not. Process this term only if the term is still failing. Otherwise ignore.
//    $asdaURLPreCheck = $asdaURLPrefix . $row[1];
//    $asda_html_pre_content = scraperwiki::scrape($asdaURLPreCheck);
//    $asda_pre_html = str_get_html($asda_html_pre_content);

//    if(isset($asda_html->find("div.showing"))){
//         $termWorkingNow = 1;
//         print $termWorkingNow . "\n";
//    }

    print $url . "\n";
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
        foreach ($html->find("div.relatedSearches a") as $el) {
            $asdaURL = $asdaURLPrefix . str_replace(" ", "+", $el->innertext);
            $asda_html_content = scraperwiki::scrape($asdaURL);
            $asda_html = str_get_html($asda_html_content);
            if($asda_html->find("div.showing")){
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
            //        print json_encode($record) . "\n";
                    scraperwiki::save(array('searchTerm'), $record); 
                    break;
                }
            }else{
                    $record = array(
                        'searchTerm' => str_replace("+"," ",$row[1]) . " - " . $el->plaintext, 
                        'relatedTerms' => str_replace("."," ",str_replace("Related Searches: "," ",$el->plaintext)),
                        'resultsFoundOnAsdaDirect' => 'false',
                        'noOfResultsFoundOnAsdaDirect' => 0
                    );
                    scraperwiki::save(array('searchTerm'), $record); 
            }
        }
       foreach ($html->find("div.didYouMean a") as $el) {
           $asdaURL = $asdaURLPrefix . str_replace(" ", "+", trim(str_replace("Did you mean: ","",$el->plaintext)));
           $asda_html_content = scraperwiki::scrape($asdaURL);
           $asda_html = str_get_html($asda_html_content);
           if ($el->plaintext != $row[1]){ //This check is added to filter terms which are same as original term. This can happen in some cases. See example for 'DEHUMIDIFER' on Amazon
               if($asda_html->find("div.showing")){
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
                //    print json_encode($record) . "\n";
                    scraperwiki::save(array('searchTerm'), $record);
                    break;
                   }
               }else{
                        $record = array(
                            'searchTerm' => str_replace("+"," ",$row[1]) . "-" . trim(str_replace("Did you mean: ","",$el->plaintext)), 
                            'didYouMean' => str_replace("Did you mean: "," ",$el->plaintext),
                            'resultsFoundOnAsdaDirect' => 'false',
                            'noOfResultsFoundOnAsdaDirect' => 0
                        );
                        scraperwiki::save(array('searchTerm'), $record); 
                }
           }
       }
}



?>
