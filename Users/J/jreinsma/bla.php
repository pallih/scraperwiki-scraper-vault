<?php

/*
#nr of houses for sale and sold in Friesland, the netherlands.
*/

require 'scraperwiki/simple_html_dom.php';           

$html_content = scraperwiki::scrape("http://www.funda.nl/koop/provincie-friesland/sorteer-datum-af/");
$html = str_get_html($html_content);


$housesForSale = $html->find("li.active a span.hits",0);
$housesForSale = $housesForSale->innertext;           
$housesForSale = str_replace(array( '(', ')' ), '', $housesForSale);

echo $housesForSale; 
echo "\n";


$e = $html->find("ul[class=link-list tab-list]",0);
//print $e->innertext . "\n";

$i = 0;
foreach($e->getElementsByTagName('li') as $li) {

echo "ja" . $li->innertext ."\n";

$i++;

if ($i == 2)
    return;
}


?>
<?php

/*
#nr of houses for sale and sold in Friesland, the netherlands.
*/

require 'scraperwiki/simple_html_dom.php';           

$html_content = scraperwiki::scrape("http://www.funda.nl/koop/provincie-friesland/sorteer-datum-af/");
$html = str_get_html($html_content);


$housesForSale = $html->find("li.active a span.hits",0);
$housesForSale = $housesForSale->innertext;           
$housesForSale = str_replace(array( '(', ')' ), '', $housesForSale);

echo $housesForSale; 
echo "\n";


$e = $html->find("ul[class=link-list tab-list]",0);
//print $e->innertext . "\n";

$i = 0;
foreach($e->getElementsByTagName('li') as $li) {

echo "ja" . $li->innertext ."\n";

$i++;

if ($i == 2)
    return;
}


?>
