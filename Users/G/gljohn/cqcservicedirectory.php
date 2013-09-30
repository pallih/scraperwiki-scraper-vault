<?php

$data = scraperWiki::scrape('http://www.cqc.org.uk/sites/default/files/cqc_locations_export.csv');
$lines = explode("\n", $data);
//Move lines on as header is on line 5 (is there a better way round this?
$header = str_getcsv(array_shift($lines)); 
$header = str_getcsv(array_shift($lines));
$header = str_getcsv(array_shift($lines)); 
$header = str_getcsv(array_shift($lines)); 
$header = str_getcsv(array_shift($lines)); 
//var_dump($header);

foreach($lines as $row) { 
    $row = str_getcsv($row); 
    if ($row[0]) { 
        $record = array_combine($header, $row); 
        scraperwiki::save(array('Name',
                                'Address', 
                                'Postcode', 
                                'Phone number', 
                                'Service\'s website (if available)', 
                                'Service types', 
                                'Date of latest check', 
                                'Specialisms/services', 
                                'Provider name', 
                                'Local Authority', 
                                'Region', 
                                'Location URL', 
                                'CQC Location ID (for office use only)', 
                                'CQC Provider ID (for office use only)'), 
                                $record);
    }
}

?>
<?php

$data = scraperWiki::scrape('http://www.cqc.org.uk/sites/default/files/cqc_locations_export.csv');
$lines = explode("\n", $data);
//Move lines on as header is on line 5 (is there a better way round this?
$header = str_getcsv(array_shift($lines)); 
$header = str_getcsv(array_shift($lines));
$header = str_getcsv(array_shift($lines)); 
$header = str_getcsv(array_shift($lines)); 
$header = str_getcsv(array_shift($lines)); 
//var_dump($header);

foreach($lines as $row) { 
    $row = str_getcsv($row); 
    if ($row[0]) { 
        $record = array_combine($header, $row); 
        scraperwiki::save(array('Name',
                                'Address', 
                                'Postcode', 
                                'Phone number', 
                                'Service\'s website (if available)', 
                                'Service types', 
                                'Date of latest check', 
                                'Specialisms/services', 
                                'Provider name', 
                                'Local Authority', 
                                'Region', 
                                'Location URL', 
                                'CQC Location ID (for office use only)', 
                                'CQC Provider ID (for office use only)'), 
                                $record);
    }
}

?>
