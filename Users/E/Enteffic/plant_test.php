<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://farm.autotrader.co.uk/categorysubcategory/category/tractors/subcategory/compact-tractor/subcategory/large-tractor/subcategory/medium-tractor/subcategory/other-tractors/subcategory/small-tractor/search?sort=MostRecent&locationName=Preston&latitude=53.76667&longitude=-2.71667&postcode=PR2");
$html = str_get_html($html_content);


foreach ($html->find("h2.advertTitle a") as $Model) {

//    print $make . "\n";
//    print $make->href . "\n";
//    print $make->innertext . "\n";

// print json_encode($make->innertext) . "\n"; 

scraperwiki::save_sqlite(array("Latest Tractors for for Sale in Preston"),array("Latest Tractors for for Sale in Preston"=>"$Model->innertext",));
//scraperwiki::save_sqlite(array("Price"),array("Price"=>"$Price->innertext",));
}
//scraperwiki::save_sqlite(array("$URL->innertext"),array("$URL->innertext"=>1, "$URL->innertext"=>"$URL->innertext"));



?>
<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://farm.autotrader.co.uk/categorysubcategory/category/tractors/subcategory/compact-tractor/subcategory/large-tractor/subcategory/medium-tractor/subcategory/other-tractors/subcategory/small-tractor/search?sort=MostRecent&locationName=Preston&latitude=53.76667&longitude=-2.71667&postcode=PR2");
$html = str_get_html($html_content);


foreach ($html->find("h2.advertTitle a") as $Model) {

//    print $make . "\n";
//    print $make->href . "\n";
//    print $make->innertext . "\n";

// print json_encode($make->innertext) . "\n"; 

scraperwiki::save_sqlite(array("Latest Tractors for for Sale in Preston"),array("Latest Tractors for for Sale in Preston"=>"$Model->innertext",));
//scraperwiki::save_sqlite(array("Price"),array("Price"=>"$Price->innertext",));
}
//scraperwiki::save_sqlite(array("$URL->innertext"),array("$URL->innertext"=>1, "$URL->innertext"=>"$URL->innertext"));



?>
