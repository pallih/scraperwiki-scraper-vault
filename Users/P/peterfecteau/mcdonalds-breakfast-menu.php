<?php
require  'scraperwiki/simple_html_dom.php';

 $html = scraperwiki::scrape('http://www.amazon.com/b/ref=sr_aj?node=328983011&ajr=0');
 echo $html;

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('td') as $data)
{
    print $data->plaintext . "\n";
}

foreach($dom->find('td') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}
?>