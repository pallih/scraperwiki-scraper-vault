<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/?f=a&th=1&q=p%C3%A9niche");


# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.ad-lbc") as $data)
{
    $entry = array();
    $entry['ville'] = $data->find("placement")
 }


?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/?f=a&th=1&q=p%C3%A9niche");


# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.ad-lbc") as $data)
{
    $entry = array();
    $entry['ville'] = $data->find("placement")
 }


?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/?f=a&th=1&q=p%C3%A9niche");


# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.ad-lbc") as $data)
{
    $entry = array();
    $entry['ville'] = $data->find("placement")
 }


?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.leboncoin.fr/ventes_immobilieres/offres/ile_de_france/?f=a&th=1&q=p%C3%A9niche");


# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.ad-lbc") as $data)
{
    $entry = array();
    $entry['ville'] = $data->find("placement")
 }


?>