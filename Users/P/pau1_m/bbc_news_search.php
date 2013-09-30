<?php


require 'scraperwiki/simple_html_dom.php';    

$keywords = 'taxi news';

$base_url = 'http://www.bbc.co.uk/search/?q=';

$query = $base_url . $keywords;

$page = scraperWiki::scrape($query);

print_r($page);

$dom = new simple_html_dom(); 
$dom->load($page);

$articles = $dom->find('.lead');

print_r($articles);


?>
<?php


require 'scraperwiki/simple_html_dom.php';    

$keywords = 'taxi news';

$base_url = 'http://www.bbc.co.uk/search/?q=';

$query = $base_url . $keywords;

$page = scraperWiki::scrape($query);

print_r($page);

$dom = new simple_html_dom(); 
$dom->load($page);

$articles = $dom->find('.lead');

print_r($articles);


?>
