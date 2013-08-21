<?php
/**
 * Number of charities each day.  Allows some query params.
 * Scraped from Charity Commission.
 */

/**
 * Params allowed:
 *
 * dateFrom        A date in Y-m-d format (e.g. 2012-05-01).  Optional: if not passed, uses last 3 months
 * dateTo          A date in Y-m-d format (e.g. 2012-05-01).  Optional: if not passed, uses today
 * stat            The stat to use: one of 'numMainCharities', 'numTotalCharities', 'numLinkedCharities', or 'all'. Default 'all'
 *
 * Will return a json-encoded array of objects, with keys 'date' and the stat passed, or all of them, in ascending date order:
 * [{"date":"2012-05-01","numMainCharities":"162229"}, {"date":"2012-05-02","numMainCharities":"162228"}...]
 *
 * If there are no data for any of the dates specified, you won't get anything, not even empty objects.
 *
 * The data only become available from 1st May 2012, so don't try going back before then.
 */ 

scraperwiki::httpresponseheader("Content-Type","text/json");
$sourcescraper = 'charitycommissiondailynumcharities';
scraperwiki::attach($sourcescraper);

// query params:

// set defaults:
$defaultDateFrom = date('Y-m-d', strtotime('-3 months'));
$defaultDateTo = date('Y-m-d');
$validStats = array('numMainCharities', 'numTotalCharities', 'numLinkedCharities', 'all');

// get params passed, or use defaults.  Check stat is valid if passed
$dateFrom = (array_key_exists('dateFrom', $_GET) ? $_GET['dateFrom'] : $defaultDateFrom);
$dateTo = (array_key_exists('dateTo', $_GET) ? $_GET['dateTo'] : $defaultDateTo);
$stat = (array_key_exists('stat', $_GET) && in_array($_GET['stat'], $validStats) ? 
    $_GET['stat'] :
    'all');
$callback = (array_key_exists('callback', $_GET) ? $_GET['callback'] : '');


// some validation:
if (!(date('Y-m-d', strtotime($dateFrom)))) {
     $dateFrom = $defaultDateFrom;
}
if (!(date('Y-m-d', strtotime($dateTo)))) {
     $dateTo = $defaultDateTo;
}
// strings for the dates
$dateFrom .= 'T00:00:00';
$dateTo .= 'T23:59:59';

// the sql:
$sql = "* from charitycommissiondailynumcharities.swdata "
     . " where `date` >= '" . $dateFrom . "'"
    . " and `date` <= '" .$dateTo . "'"  
    . " ORDER BY `date` ASC";

$data = scraperwiki::select($sql);
// echo $sql;

// parse the data for return:
$ret = array();
foreach ($data as $d) {

    $row = new stdClass();
    $row->date = date('Y-m-d', strtotime($d['date']));
    if ($stat == 'all') {
        $row->numMainCharities = $d['numMainCharities'];
        $row->numTotalCharities = $d['numTotalCharities'];
        $row->numLinkedCharities = $d['numLinkedCharities'];
    } else {
        $row->{$stat} = $d[$stat];
    }

    $ret[] = $row;
        
}
//var_dump($ret);

// give 'em some json:
if ($callback) {
    echo $callback . '(';
}
echo json_encode($ret);
if ($callback) {
    echo ');';
}
?>