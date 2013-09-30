<?php

$html = scraperWiki::scrape("http://www.amazon.co.uk/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=surround+sound");


require 'scraperwiki/simple_html_dom.php'; 

$data = scraperWiki::scrape('http://leapgradient.com/asda/Test_File_for_Amazon_Scrap.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $url= 'http://www.ebay.co.uk/sch/i.html?_nkw=' . $row[1];
 //   print $url;
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
 //   print $html;
        foreach ($html->find("div#RelatedSearchesDF") as $el) {
         print "inside for";
         //   print $el->innertext . "\n";
            $record = array(
                'searchTerm' => $row[0], 
                'relatedTerms' => str_replace("\t\t  "," ",str_replace("&nbsp;"," ",str_replace("  \t\tRelated searches:&nbsp;  \t\t\t  \t\t\t\t"," ",$el->plaintext)))
            );
            print json_encode($record) . "\n";
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
    $url= 'http://www.ebay.co.uk/sch/i.html?_nkw=' . $row[1];
 //   print $url;
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
 //   print $html;
        foreach ($html->find("div#RelatedSearchesDF") as $el) {
         print "inside for";
         //   print $el->innertext . "\n";
            $record = array(
                'searchTerm' => $row[0], 
                'relatedTerms' => str_replace("\t\t  "," ",str_replace("&nbsp;"," ",str_replace("  \t\tRelated searches:&nbsp;  \t\t\t  \t\t\t\t"," ",$el->plaintext)))
            );
            print json_encode($record) . "\n";
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
    $url= 'http://www.ebay.co.uk/sch/i.html?_nkw=' . $row[1];
 //   print $url;
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
 //   print $html;
        foreach ($html->find("div#RelatedSearchesDF") as $el) {
         print "inside for";
         //   print $el->innertext . "\n";
            $record = array(
                'searchTerm' => $row[0], 
                'relatedTerms' => str_replace("\t\t  "," ",str_replace("&nbsp;"," ",str_replace("  \t\tRelated searches:&nbsp;  \t\t\t  \t\t\t\t"," ",$el->plaintext)))
            );
            print json_encode($record) . "\n";
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
    $url= 'http://www.ebay.co.uk/sch/i.html?_nkw=' . $row[1];
 //   print $url;
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
 //   print $html;
        foreach ($html->find("div#RelatedSearchesDF") as $el) {
         print "inside for";
         //   print $el->innertext . "\n";
            $record = array(
                'searchTerm' => $row[0], 
                'relatedTerms' => str_replace("\t\t  "," ",str_replace("&nbsp;"," ",str_replace("  \t\tRelated searches:&nbsp;  \t\t\t  \t\t\t\t"," ",$el->plaintext)))
            );
            print json_encode($record) . "\n";
            scraperwiki::save(array('searchTerm'), $record); 
        }
}



?>
