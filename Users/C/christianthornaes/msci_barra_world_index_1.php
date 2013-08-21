<?php

#$data = scraperWiki::scrape('http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv');

$data = scraperWiki::scrape('http://www.mscibarra.com/products/indices/performance/regional_chart.html?priceLevel=0&scope=R&style=C&asOf=Dec%2019,%202011&currency=15&size=36&indexId=106#');

function print_date($when) {           
    print $when->format(DATE_ISO8601) . "\n"; 
}

$when = date_create('21 June 2010'); print_date($when); # 2010-06-21T00:00:00+0100
$when = date_create('10-Jul-1899'); print_date($when);  # 1899-07-10T00:00:00+0000
$when = date_create('01/01/01'); print_date($when);     # 2001-01-01T00:00:00+0000

print get_class(date_create('21 June 2010')) . "\n"; # DateTime

$lines = explode("\n", $data);

#foreach($lines as $row) {           
#    $row = str_getcsv($row);
#    printf("Index Level \n", $row[8], $row[3]);
#}

$header = str_getcsv(array_shift($lines));

foreach($lines as $row) {           
    $row = str_getcsv($row);
    if ($row[7]) {
        $record = array_combine($header, $row);
        $record['Amount'] = (float)$record['Amount'];
        scraperwiki::save(array('Date', 'Index'), $record);
    }
}

?>
