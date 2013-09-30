<?php

// documentation
// https://scraperwiki.com/docs/php/php_css_guide/

require 'scraperwiki/simple_html_dom.php';

// variable to scrape
$urlParking = scraperWiki::scrape("http://www.cityofmadison.com/parkingUtility/garagesLots/availability/");

$pageParking = new simple_html_dom();

$pageParking->load($urlParking);

$divParking = $pageParking->find("div#availability");

print $divParking;

?>
<?php

// documentation
// https://scraperwiki.com/docs/php/php_css_guide/

require 'scraperwiki/simple_html_dom.php';

// variable to scrape
$urlParking = scraperWiki::scrape("http://www.cityofmadison.com/parkingUtility/garagesLots/availability/");

$pageParking = new simple_html_dom();

$pageParking->load($urlParking);

$divParking = $pageParking->find("div#availability");

print $divParking;

?>
