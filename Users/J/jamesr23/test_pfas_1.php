<?php

$data = scraperWiki::scrape('https://secure.38degrees.org.uk/page/-/documents/pfa-postcode%20for%20bsd%20tool%20test.csv');
str_replace($data,'"','');
$lines = explode("\n", $data); 

$j = 0;

## Include DOM Script
require 'scraperwiki/simple_html_dom.php';     
$dom = new simple_html_dom();


foreach($lines as $row) {
$row = str_getcsv($row);
echo $row[1] . $row[0] . str_replace(' ','%20',$row[1]);

$html = scraperWiki::scrape('https://secure.38degrees.org.uk/page/speakout/bsdtest?js=false&zip=' . str_replace(' ','%20',$row[1]));

## Extract the Person's name from the HTML ##
#############################################
$dom->load($html);

foreach($dom->find("span[@class='recipient-name']") as $data){
$name = strip_tags($data);
}
################################################

$record = array(
            'id' => $j,
            'postcode' => $row[1],
            'policearea' => $row[0],
             'bsd_name' => $name     
        );
scraperwiki::save(array('id'), $record);

usleep(1000);

$j++;

}

?><?php

$data = scraperWiki::scrape('https://secure.38degrees.org.uk/page/-/documents/pfa-postcode%20for%20bsd%20tool%20test.csv');
str_replace($data,'"','');
$lines = explode("\n", $data); 

$j = 0;

## Include DOM Script
require 'scraperwiki/simple_html_dom.php';     
$dom = new simple_html_dom();


foreach($lines as $row) {
$row = str_getcsv($row);
echo $row[1] . $row[0] . str_replace(' ','%20',$row[1]);

$html = scraperWiki::scrape('https://secure.38degrees.org.uk/page/speakout/bsdtest?js=false&zip=' . str_replace(' ','%20',$row[1]));

## Extract the Person's name from the HTML ##
#############################################
$dom->load($html);

foreach($dom->find("span[@class='recipient-name']") as $data){
$name = strip_tags($data);
}
################################################

$record = array(
            'id' => $j,
            'postcode' => $row[1],
            'policearea' => $row[0],
             'bsd_name' => $name     
        );
scraperwiki::save(array('id'), $record);

usleep(1000);

$j++;

}

?>