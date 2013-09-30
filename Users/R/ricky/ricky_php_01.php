<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://everguide.com.au/melbourne/event/2012-jun-21/school-of-seven-bells");

$dom = new simple_html_dom();
$dom->load($html);

       
$el = $dom->find('span[itemprop=name]',0);   

print $el . "\n";
$str = $html;
echo $html; 

?>
<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://everguide.com.au/melbourne/event/2012-jun-21/school-of-seven-bells");

$dom = new simple_html_dom();
$dom->load($html);

       
$el = $dom->find('span[itemprop=name]',0);   

print $el . "\n";
$str = $html;
echo $html; 

?>
