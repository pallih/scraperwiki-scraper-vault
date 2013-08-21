<?php

$asdaURLPrefix = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=';
$asdaURLSuffix = '&domainName=Products&headerVersion=v1&_requestid=420413';

require 'scraperwiki/simple_html_dom.php'; 

$data = scraperWiki::scrape('http://leapgradient.com/asda/Test_File_for_ASDA_Groceries_Scrap_test.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $keyword= $row[0];
    $url = $asdaURLPrefix . $keyword . $asdaURLSuffix ;
    print $url . "\n";
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
    print $html . "\n";
        foreach ($html->find("div#facetedSearch") as $el) {
            print $el->innertext . "\n";
            $asdaURL = $asdaURLPrefix . str_replace(" ", "+", $el->innertext);
  //          $asda_html_content = scraperwiki::scrape($asdaURL);
  //          $asda_html = str_get_html($asda_html_content);
  //          foreach ($asda_html->find("div.showing") as $asdaResultSet) {
  //              $resultCountText = $asdaResultSet->plaintext;
  //              preg_match('/ of [0-9\.\-]*/', $resultCountText, $matches);
  //              $resultCount = str_replace(" of ", "", $matches[0]) . "\n";
  //              $record = array(
  //                  'searchTerm' => str_replace("+"," ",$row[1]) . " - " . $el->plaintext, 
  //                  'relatedTerms' => str_replace("."," ",str_replace("Related Searches: "," ",$el->plaintext)),
  //                  'resultsFoundOnAsdaDirect' => 'true',
  //                  'noOfResultsFoundOnAsdaDirect' => $resultCount
  //              );
  //      //        print json_encode($record) . "\n";
  //              scraperwiki::save(array('searchTerm'), $record); 
  //              break;
  //          }
        }
}



?>
<?php

$asdaURLPrefix = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=';
$asdaURLSuffix = '&domainName=Products&headerVersion=v1&_requestid=420413';

require 'scraperwiki/simple_html_dom.php'; 

$data = scraperWiki::scrape('http://leapgradient.com/asda/Test_File_for_ASDA_Groceries_Scrap_test.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $keyword= $row[0];
    $url = $asdaURLPrefix . $keyword . $asdaURLSuffix ;
    print $url . "\n";
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
    print $html . "\n";
        foreach ($html->find("div#facetedSearch") as $el) {
            print $el->innertext . "\n";
            $asdaURL = $asdaURLPrefix . str_replace(" ", "+", $el->innertext);
  //          $asda_html_content = scraperwiki::scrape($asdaURL);
  //          $asda_html = str_get_html($asda_html_content);
  //          foreach ($asda_html->find("div.showing") as $asdaResultSet) {
  //              $resultCountText = $asdaResultSet->plaintext;
  //              preg_match('/ of [0-9\.\-]*/', $resultCountText, $matches);
  //              $resultCount = str_replace(" of ", "", $matches[0]) . "\n";
  //              $record = array(
  //                  'searchTerm' => str_replace("+"," ",$row[1]) . " - " . $el->plaintext, 
  //                  'relatedTerms' => str_replace("."," ",str_replace("Related Searches: "," ",$el->plaintext)),
  //                  'resultsFoundOnAsdaDirect' => 'true',
  //                  'noOfResultsFoundOnAsdaDirect' => $resultCount
  //              );
  //      //        print json_encode($record) . "\n";
  //              scraperwiki::save(array('searchTerm'), $record); 
  //              break;
  //          }
        }
}



?>
