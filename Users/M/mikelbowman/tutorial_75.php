<?php

$html = scraperWiki::scrape("http://www.shopgoodwill.com/search/SearchKey.asp?itemTitle=&catid=0&sellerID=73&closed=no&minPrice=&maxPrice=&sortBy=itemEndTime&SortOrder=a&showthumbs=on");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("h1") as $data){
    
        scraperwiki::save($data);

    }


?>
<?php

$html = scraperWiki::scrape("http://www.shopgoodwill.com/search/SearchKey.asp?itemTitle=&catid=0&sellerID=73&closed=no&minPrice=&maxPrice=&sortBy=itemEndTime&SortOrder=a&showthumbs=on");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("h1") as $data){
    
        scraperwiki::save($data);

    }


?>
