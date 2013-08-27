<?php

$html = scraperWiki::scrape("http://www.amazon.co.uk/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=surround+sound");


require 'scraperwiki/simple_html_dom.php'; 

$data = scraperWiki::scrape('http://leapgradient.com/asda/Test_File_for_Amazon_Scrap.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $url= $row[2];
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
        foreach ($html->find("div.relatedSearches") as $el) {
         //   print $el->innertext . "\n";
            $record = array(
                'searchTerm' => str_replace("+"," ",$row[1]), 
                'relatedTerms' => str_replace("."," ",str_replace("Related Searches: "," ",$el->plaintext))
            );
          //  print json_encode($record) . "\n";
            scraperwiki::save(array('searchTerm'), $record); 
        }
       foreach ($html->find("div.didYouMean") as $el) {
         //   print $el->innertext . "\n";
           $record = array(
                'searchTerm' => str_replace("+"," ",$row[1]), 
                'didYouMean' => str_replace("Did you mean: "," ",$el->plaintext)
            );
          //  print json_encode($record) . "\n";
            scraperwiki::save(array('searchTerm'), $record); 
        }
}



?>
<?php

$html = scraperWiki::scrape("http://www.amazon.co.uk/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=surround+sound");


require 'scraperwiki/simple_html_dom.php'; 

$data = scraperWiki::scrape('http://leapgradient.com/asda/Test_File_for_Amazon_Scrap.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $url= $row[2];
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
        foreach ($html->find("div.relatedSearches") as $el) {
         //   print $el->innertext . "\n";
            $record = array(
                'searchTerm' => str_replace("+"," ",$row[1]), 
                'relatedTerms' => str_replace("."," ",str_replace("Related Searches: "," ",$el->plaintext))
            );
          //  print json_encode($record) . "\n";
            scraperwiki::save(array('searchTerm'), $record); 
        }
       foreach ($html->find("div.didYouMean") as $el) {
         //   print $el->innertext . "\n";
           $record = array(
                'searchTerm' => str_replace("+"," ",$row[1]), 
                'didYouMean' => str_replace("Did you mean: "," ",$el->plaintext)
            );
          //  print json_encode($record) . "\n";
            scraperwiki::save(array('searchTerm'), $record); 
        }
}



?>
<?php

$html = scraperWiki::scrape("http://www.amazon.co.uk/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=surround+sound");


require 'scraperwiki/simple_html_dom.php'; 

$data = scraperWiki::scrape('http://leapgradient.com/asda/Test_File_for_Amazon_Scrap.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $url= $row[2];
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
        foreach ($html->find("div.relatedSearches") as $el) {
         //   print $el->innertext . "\n";
            $record = array(
                'searchTerm' => str_replace("+"," ",$row[1]), 
                'relatedTerms' => str_replace("."," ",str_replace("Related Searches: "," ",$el->plaintext))
            );
          //  print json_encode($record) . "\n";
            scraperwiki::save(array('searchTerm'), $record); 
        }
       foreach ($html->find("div.didYouMean") as $el) {
         //   print $el->innertext . "\n";
           $record = array(
                'searchTerm' => str_replace("+"," ",$row[1]), 
                'didYouMean' => str_replace("Did you mean: "," ",$el->plaintext)
            );
          //  print json_encode($record) . "\n";
            scraperwiki::save(array('searchTerm'), $record); 
        }
}



?>
