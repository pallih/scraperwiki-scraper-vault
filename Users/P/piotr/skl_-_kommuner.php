<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.skl.se/kommuner_och_landsting/om_kommuner/kommuner");
//print $html;

$dom = new simple_html_dom();
$dom->load($html);

$maindiv = $dom->find('div.MarginPageTop');
$maindiv = $maindiv[0];

foreach($maindiv->find('div.Text') as $data)
{
    
    $datatemp = trim($data->find('a', 0)->plaintext);

    print "DATA: " . $datatemp . "\n";
    scraperwiki::save(array('data'), array('data' => $datatemp));
}

?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.skl.se/kommuner_och_landsting/om_kommuner/kommuner");
//print $html;

$dom = new simple_html_dom();
$dom->load($html);

$maindiv = $dom->find('div.MarginPageTop');
$maindiv = $maindiv[0];

foreach($maindiv->find('div.Text') as $data)
{
    
    $datatemp = trim($data->find('a', 0)->plaintext);

    print "DATA: " . $datatemp . "\n";
    scraperwiki::save(array('data'), array('data' => $datatemp));
}

?>