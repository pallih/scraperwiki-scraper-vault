<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/?f=a&th=1&q=peniche");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('div.list-ads a') as $data)
{
    $entry = array();
    $entry['url'] = $data->getAttribute('href');
    $entry['titre'] = $data->find('href.title');
    print "TITRE ".$entry['titre']. "\n";
    print "TITRE ".$data->find('href.title'). "\n";

 }

?>

