<?php

$data = scraperWiki::scrape('https://secure.38degrees.org.uk/page/-/documents/Police%20force%20areas%20and%20LatLng%20for%20testing.csv');
str_replace($data,'"','');
$lines = explode("\n", $data); 

for ($i=0; $i<300; $i++){
unset($lines[$i]);
}

foreach($lines as $row) {
$row = str_getcsv($row);
$json = scraperWiki::scrape('http://policeapi2.rkh.co.uk/api/locate-neighbourhood?q=' . $row[3] . ',' . $row[4]);

$record = array(
'cons' => $row[0],
            'postcode' => $row[2],
            'force' => $row[1],
            'json' => $json            
        );
        scraperwiki::save(array('cons'), $record);
usleep(100000);
}

?><?php

$data = scraperWiki::scrape('https://secure.38degrees.org.uk/page/-/documents/Police%20force%20areas%20and%20LatLng%20for%20testing.csv');
str_replace($data,'"','');
$lines = explode("\n", $data); 

for ($i=0; $i<300; $i++){
unset($lines[$i]);
}

foreach($lines as $row) {
$row = str_getcsv($row);
$json = scraperWiki::scrape('http://policeapi2.rkh.co.uk/api/locate-neighbourhood?q=' . $row[3] . ',' . $row[4]);

$record = array(
'cons' => $row[0],
            'postcode' => $row[2],
            'force' => $row[1],
            'json' => $json            
        );
        scraperwiki::save(array('cons'), $record);
usleep(100000);
}

?><?php

$data = scraperWiki::scrape('https://secure.38degrees.org.uk/page/-/documents/Police%20force%20areas%20and%20LatLng%20for%20testing.csv');
str_replace($data,'"','');
$lines = explode("\n", $data); 

for ($i=0; $i<300; $i++){
unset($lines[$i]);
}

foreach($lines as $row) {
$row = str_getcsv($row);
$json = scraperWiki::scrape('http://policeapi2.rkh.co.uk/api/locate-neighbourhood?q=' . $row[3] . ',' . $row[4]);

$record = array(
'cons' => $row[0],
            'postcode' => $row[2],
            'force' => $row[1],
            'json' => $json            
        );
        scraperwiki::save(array('cons'), $record);
usleep(100000);
}

?>