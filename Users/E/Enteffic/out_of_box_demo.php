<?php

$html = scraperWiki::scrape("http://farm.autotrader.co.uk/categorysubcategory/category/tractors/subcategory/compact-tractor/subcategory/large-tractor/subcategory/medium-tractor/subcategory/other-tractors/subcategory/small-tractor/search?sort=PriceDesc&locationName=Preston&latitude=53.76667&longitude=-2.71667&postcode=PR2");
print $html . "\n";


require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("h2.advertTitle a") as $make){
scraperwiki::save(array('make'), $record);

    }




?>
<?php

$html = scraperWiki::scrape("http://farm.autotrader.co.uk/categorysubcategory/category/tractors/subcategory/compact-tractor/subcategory/large-tractor/subcategory/medium-tractor/subcategory/other-tractors/subcategory/small-tractor/search?sort=PriceDesc&locationName=Preston&latitude=53.76667&longitude=-2.71667&postcode=PR2");
print $html . "\n";


require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("h2.advertTitle a") as $make){
scraperwiki::save(array('make'), $record);

    }




?>
