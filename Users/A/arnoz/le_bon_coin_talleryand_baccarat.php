<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.leboncoin.fr/annonces/offres/ile_de_france/?f=a&th=1&q=baccarat+talleyrand");


# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('div.list-lbc a') as $data)
{
    $entry = array();
    $entry['url'] = $data->find('href',0);
    $entry['titre'] = $data->find('div[class=title]', 0)->plaintext;
    print "TITRE ".$entry['titre']. "\n";


 }

?>
