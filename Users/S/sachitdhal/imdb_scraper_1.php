<?php

$html = scraperWiki::scrape("http://academic.research.microsoft.com/RankList?entitytype=2&topdomainid=2&subdomainid=5&last=0&orderby=1");

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


while(true)
    {
foreach($dom->find("td[@class='staticOrderCol']") as $swiki);
    print $swiki . "\n";
}

?>
<?php

$html = scraperWiki::scrape("http://academic.research.microsoft.com/RankList?entitytype=2&topdomainid=2&subdomainid=5&last=0&orderby=1");

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);


while(true)
    {
foreach($dom->find("td[@class='staticOrderCol']") as $swiki);
    print $swiki . "\n";
}

?>
