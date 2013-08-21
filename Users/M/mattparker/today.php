<?php
# Blank PHP
$sourcescraper = 'charitycommissiondailynumcharities';
scraperwiki::attach($sourcescraper);

$dateFrom = date('Y-m-d') . 'T00:00:00';
$dateTo = date('Y-m-d') . 'T23:59:59';
$sql = "* from charitycommissiondailynumcharities.swdata "
     . " where `date` >= '" . $dateFrom . "'"
    . " and `date` <= '" .$dateTo . "'";
$data = scraperwiki::select($sql);
//var_dump($data);

echo json_encode($data[0]);
?>
