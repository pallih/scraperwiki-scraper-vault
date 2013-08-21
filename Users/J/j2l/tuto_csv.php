<?php

$data = scraperWiki::scrape('https://docs.google.com/spreadsheet/pub?key=0AvHXbsdaE2-ZdHJSTm1KU3pNazJFeXpEQTc3TnlNSkE&single=true&gid=0&output=csv');
$lines = explode("\n", $data);           
foreach($lines as $row) {           
    $row = str_getcsv($row);
    printf("%s spent on %s\n", $row[0], $row[1]);
}
$header = str_getcsv(array_shift($lines));
foreach($lines as $row) {
    $row = str_getcsv($row);
    if ($row[0]) {
        $record = array_combine($header, $row);
        //$record['Amount'] = $record['Amount'];
        scraperwiki::save(array('headA', 'headB'), $record);
    }
}
?>
