<?php
require 'scraperwiki/simple_html_dom.php';

# Blank PHP
// http://oga.pcusa.org/section/departments/mid-councils/directory-a-m/
function scrape_pby_office()
{
    $url = "http://oga.pcusa.org/section/departments/mid-councils/directory-a-m/";
print "URL=" . $url . "\n"; 
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    foreach($dom->find("<a") as $tds)
    {
    if (substr($tds,0, 8) == "<a name=")
        {
foreach($tds as $y)
        print $y . "\n";
        //print "tds=" . $tds . "\n";
//break;
        }
    }
}
scrape_pby_office();

?>
