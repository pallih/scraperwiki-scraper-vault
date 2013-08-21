<?php
require  'scraperwiki/simple_html_dom.php';

 $html = scraperwiki::scrape('http://www.watcharena.com//luxury-watches/a-lange-sohne-limited-edition-luna-mundi-matched-set-white-and-red-gold.html');
 echo $html;

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('<tr><td>Availability:</td><td>') as $data)
{
    print $data->plaintext . "\n";
}

foreach($dom->find('<tr><td>Availability:</td><td>') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}
?>