<?php
require 'scraperwiki/simple_html_dom.php';

date_default_timezone_set('UTC');

$contents = scraperwiki::scrape("http://www.eia.gov/cneaf/electricity/epm/table1_17_a.html");
$dom = new simple_html_dom();
$dom->load($contents);

$headers = array('Census Division and State', 'Feb-11', 'Feb-10', 'Percent Change');

$section = '';
$current_month = '';
$previous_month = '';

$values = $dom->find('table tr td.headrow1');
foreach ($values as $v) {
    $date = date_parse_from_format('b-y', $v->plaintext);
    
    if (is_array($date) && count($date['errors']) === 0) {
        print_r($date);
    } else {
        print_r(array($date['errors'], $v->plaintext));
    }
}
exit;


foreach($dom->find('td table tr') as $data){  

    $tds = $data->find('td');
    if (count($tds) !== 12) {
        continue;
    }

    foreach ($tds as $td) {
        // this is a header row
        if ($td->class === "headrow1") {
            $headers[1] = $td->plaintext;
        }
    }

    // var_dump($tds[0]->class);
    // exit;
     //       if ($current_month) $headers[1] = $current_month;
        //    if ($previous_month) $headers[2] = $previous_month;


    $tdcounter = 0;

    $record = array( );

    foreach ($tds as $td) {
        if ($td->class === "headrow1") {
            switch ($tdcounter++) {
                case 0:
                    $section = $td->plaintext;
                    break;
                case 1:
                    $current_month = $td->plaintext;
                    break;
                case 2:
                    $previous_month = $td->plaintext;
                    break;
                default:
                    // print $tdcounter . "\n";
                    break;
            }
        } else {
            if ($section) $record['Section'] = $section;

            $header_text = $headers[$tdcounter];
            if (! $header_text) continue;
            $record[$header_text] = $td->plaintext;
        }
        // print sprintf("%s - %s\n", $section, $td->plaintext);
    }

    // print_r($record);
    // print "\n";

/*    $record = array(
        'name' => $name, 
        'order' => $order,
        'last_updated' => date('Y-m-d H:i:s'),
    ); */

//    array_push($records, $record);
}

// scraperwiki::save(array('ICAO'), $records);
