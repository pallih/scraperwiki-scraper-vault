<?php

scraperwiki::sqliteexecute("delete from swdata"); 
scraperwiki::sqlitecommit();

$asdaURLPrefix = 'http://direct.asda.com/on/demandware.store/Sites-ASDA-Site/default/Search-Show?q=';

require 'scraperwiki/simple_html_dom.php'; 

$data = scraperWiki::scrape('http://leapgradient.com/asda/ASDA_Direct_Sitemap.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $url= $row[0] . ","  . $row[1] . ","  . $row[2];
  //  print $url . "\n";

    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
        foreach ($html->find("div.featuredProducts_pm") as $el) {
       //     print $el->plaintext. "\n";
               $pos1 = strpos($el->plaintext, 'Empty carousel products.');
               $pos2 = strpos($el->plaintext, 'No products found');
                if ($pos1 !== false || $pos2 !== false) {
                   print $url . "\n";
                   $record = array(
                        'url' => $url, 
                    );
                    scraperwiki::save(array('url'), $record); 
                    break;
                }
        }
}



?>
<?php

scraperwiki::sqliteexecute("delete from swdata"); 
scraperwiki::sqlitecommit();

$asdaURLPrefix = 'http://direct.asda.com/on/demandware.store/Sites-ASDA-Site/default/Search-Show?q=';

require 'scraperwiki/simple_html_dom.php'; 

$data = scraperWiki::scrape('http://leapgradient.com/asda/ASDA_Direct_Sitemap.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $url= $row[0] . ","  . $row[1] . ","  . $row[2];
  //  print $url . "\n";

    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
        foreach ($html->find("div.featuredProducts_pm") as $el) {
       //     print $el->plaintext. "\n";
               $pos1 = strpos($el->plaintext, 'Empty carousel products.');
               $pos2 = strpos($el->plaintext, 'No products found');
                if ($pos1 !== false || $pos2 !== false) {
                   print $url . "\n";
                   $record = array(
                        'url' => $url, 
                    );
                    scraperwiki::save(array('url'), $record); 
                    break;
                }
        }
}



?>
<?php

scraperwiki::sqliteexecute("delete from swdata"); 
scraperwiki::sqlitecommit();

$asdaURLPrefix = 'http://direct.asda.com/on/demandware.store/Sites-ASDA-Site/default/Search-Show?q=';

require 'scraperwiki/simple_html_dom.php'; 

$data = scraperWiki::scrape('http://leapgradient.com/asda/ASDA_Direct_Sitemap.csv');

$lines = explode("\n", $data);

foreach($lines as $row) {
    $row = str_getcsv($row);
    $url= $row[0] . ","  . $row[1] . ","  . $row[2];
  //  print $url . "\n";

    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
        foreach ($html->find("div.featuredProducts_pm") as $el) {
       //     print $el->plaintext. "\n";
               $pos1 = strpos($el->plaintext, 'Empty carousel products.');
               $pos2 = strpos($el->plaintext, 'No products found');
                if ($pos1 !== false || $pos2 !== false) {
                   print $url . "\n";
                   $record = array(
                        'url' => $url, 
                    );
                    scraperwiki::save(array('url'), $record); 
                    break;
                }
        }
}



?>
