<?php


#$data = scraperWiki::scrape('http://www.mscibarra.com/products/indices/performance/regional_chart.html?priceLevel=0&scope=R&style=C&asOf=Dec%2019,%202011&currency=15&size=36&indexId=106');

$data = scraperWiki::scrape('http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv');

$lines = explode("\n", $data);

#Printing in Console Tab
foreach($lines as $row) { 
    $row = str_getcsv($row); 
    printf("£%s spent on %s\n", $row[7], $row[3]); 
}

$header = str_getcsv(array_shift($lines));

#Printing in Data Tab
foreach($lines as $row) {                
    $row = str_getcsv($row);     
    if ($row[0]) {         
        $record = array_combine($header, $row);         
        $record['Amount'] = (float)$record['Amount'];         
        scraperwiki::save(array('Transaction Number', 'Expense Type', 'Expense Area'), $record);     
    } 
}
?>
