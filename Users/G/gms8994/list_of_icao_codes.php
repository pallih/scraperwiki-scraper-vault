<?php
date_default_timezone_set('UTC');

$contents = scraperwiki::scrape("http://www.rap.ucar.edu/weather/surface/stations.txt");
$data = explode("\n", $contents);

$records = array();
foreach ($data as $line) {
    if (stripos($line, "!") === 0) continue;
    if (strlen($line) < 83) continue;

    //                     ICAO
    // AK ADAK NAS         PADK  ADK   70454  51 53N  176 39W    4   X     T          7 US

    $line = substr($line, 20, 4);

    if ($line === '    ') continue;

    $record = array(
        'ICAO' => $line,
    );

    array_push($records, $record);
}

scraperwiki::save(array('ICAO'), $records);
<?php
date_default_timezone_set('UTC');

$contents = scraperwiki::scrape("http://www.rap.ucar.edu/weather/surface/stations.txt");
$data = explode("\n", $contents);

$records = array();
foreach ($data as $line) {
    if (stripos($line, "!") === 0) continue;
    if (strlen($line) < 83) continue;

    //                     ICAO
    // AK ADAK NAS         PADK  ADK   70454  51 53N  176 39W    4   X     T          7 US

    $line = substr($line, 20, 4);

    if ($line === '    ') continue;

    $record = array(
        'ICAO' => $line,
    );

    array_push($records, $record);
}

scraperwiki::save(array('ICAO'), $records);
