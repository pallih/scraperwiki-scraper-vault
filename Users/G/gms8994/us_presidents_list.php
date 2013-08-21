<?php
require 'scraperwiki/simple_html_dom.php';

date_default_timezone_set('UTC');

$contents = scraperwiki::scrape("http://www.whitehouse.gov/about/presidents");           

$dom = new simple_html_dom();
$dom->load($contents);

foreach($dom->find('#content a') as $data){  
    $line = explode(". ", $data->plaintext);
    if (! $line[1]) continue;

    $order = intval(array_shift($line));

    $name = implode(". ", $line);    
    $record = array(
        'name' => $name, 
        'order' => $order,
        'last_updated' => date('Y-m-d H:i:s'),
    );

    scraperwiki::save(array('name'), $record);

}
