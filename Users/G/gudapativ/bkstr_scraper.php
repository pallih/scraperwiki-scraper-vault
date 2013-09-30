<?php

# Blank PHP
$html_content= scraperWiki::scrape('http://www.bkstr.com/');
require 'scraperwiki/simple_html_dom.php';

$dom = str_get_html($html_content);
#print $dom;
$array=scraperWiki::scrape('http://www.bkstr.com/webapp/wcs/stores/servlet/StoreFinderAJAX?requestType=STATESUS&pageType=FLGStoreCatalogDisplay&pageSubType=US&langId=-1&demoKey=d&stateUSAIdSelect=');
#$usaurl=str_get_html($USA_url);
#print $USA_url;

print $array;
?>
<?php

# Blank PHP
$html_content= scraperWiki::scrape('http://www.bkstr.com/');
require 'scraperwiki/simple_html_dom.php';

$dom = str_get_html($html_content);
#print $dom;
$array=scraperWiki::scrape('http://www.bkstr.com/webapp/wcs/stores/servlet/StoreFinderAJAX?requestType=STATESUS&pageType=FLGStoreCatalogDisplay&pageSubType=US&langId=-1&demoKey=d&stateUSAIdSelect=');
#$usaurl=str_get_html($USA_url);
#print $USA_url;

print $array;
?>
