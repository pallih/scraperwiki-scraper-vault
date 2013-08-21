<?php

$data = scraperWiki::scrape('https://secure.38degrees.org.uk/page/-/documents/trimmed%20postcodes%20latitude%20longitude.csv');
str_replace($data,'"','');
$lines = explode("\n", $data); 

#for ($i=0; $i<1830; $i++){
#unset($lines[$i]);
#}

foreach($lines as $row) {
$row = str_getcsv($row);
$json = scraperWiki::scrape('http://policeapi2.rkh.co.uk/api/locate-neighbourhood?q=' . $row[1] . ',' . $row[2]);
$record = array(
            'postcode' => $row[0],
            'json' => $json            
        );
        scraperwiki::save(array('postcode'), $record);
#usleep(100000);
}

?><?php

$data = scraperWiki::scrape('https://secure.38degrees.org.uk/page/-/documents/trimmed%20postcodes%20latitude%20longitude.csv');
str_replace($data,'"','');
$lines = explode("\n", $data); 

#for ($i=0; $i<1830; $i++){
#unset($lines[$i]);
#}

foreach($lines as $row) {
$row = str_getcsv($row);
$json = scraperWiki::scrape('http://policeapi2.rkh.co.uk/api/locate-neighbourhood?q=' . $row[1] . ',' . $row[2]);
$record = array(
            'postcode' => $row[0],
            'json' => $json            
        );
        scraperwiki::save(array('postcode'), $record);
#usleep(100000);
}

?>