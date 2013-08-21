<?php

$data = scraperWiki::scrape('http://cits-ltd.com/shares/cirrus/data/TN_Postcodes.csv');
$lines = explode("\n", $data);

foreach($lines as $row) {           
    $row = str_getcsv($row,',','"');
    echo $row[0]." has been saved to record."."\n";
}

$header = str_getcsv(array_shift($lines),',','"');   

foreach($lines as $row) {           
    $row = str_getcsv($row);
    if ($row[0]) {
        $record = array_combine($header, $row);

        scraperwiki::save(
            array(
                'CompanyName',
                'CompanyNumber',
                'RegAddress.CareOf',
                'RegAddress.POBox',
                'RegAddress.AddressLine1',
                'RegAddress.AddressLine2',
                'RegAddress.PostTown',
                'RegAddress.County',
                'RegAddress.Country',
                'RegAddress.PostCode',
                'IncorporationDate',
                'SICCode.SicText_1',
                'SICCode.SicText_2',
                'SICCode.SicText_3',
                'SICCode.SicText_4',
                'URI'), $record);
            }
        }


?>
