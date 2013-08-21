<?php

// $html = scraperWiki::scrape("http://www.ncdc.noaa.gov/extremes/records/");
 

require 'scraperwiki/simple_html_dom.php';           
// $dom = new simple_html_dom();
// $dom->load($html);

$html_content = scraperwiki::scrape("http://www.ncdc.noaa.gov/extremes/records/");
$html = str_get_html($html_content);

//foreach($html->find("div#daily-div tr") as $data) {
    // $tds = $data->find("td");
    // if(count($tds)==12){
    //     $record = array(
    //         'country' => $tds[0]->plaintext, 
    //         'years_in_school' => intval($tds[4]->plaintext)
    //    );
    //    print json_encode($record) . "\n";
//    print $data . "\n";
//    print "-------------------------------- \n";
//}

$it = $html->find("div#daily-div tr", 6);

print $it . "\n";

$mydate = $it->find("td", 0);
print $mydate->innertext . "\n";
$mdate = $mydate->innertext;


$highx = $it->find("td", 1);
print $highx->innertext . "\n";
$hi = $highx->innertext;

// $highn = $it->find("td", 2);
// print $highn->innertext . "\n";
// $himin = $highn->innertext;

// $lowx = $it->find("td", 3);
// print $lowx->innertext . "\n";
// $lo = $lowx->innertext;

$lown = $it->find("td", 4);
print $lown->innertext . "\n";
$lomin = $lown->innertext;


// scraperwiki::save_sqlite(array("mydate"),array("mydate"=>$mydate, "max"=>$highx, "min"=>$lowx)); 
// scraperwiki::save_sqlite(array("mydate"),array("mydate"=>"$mdate", "himax"=>"$hi", "himin"=>"$himin", "lomax"=>"$lo", "lomin"=>"$lomin")); 
scraperwiki::save_sqlite(array("mydate"),array("mydate"=>"$mdate", "himax"=>"$hi", "lomin"=>"$lomin")); 

// print_r(scraperwiki::show_tables());   

// $info = scraperwiki::table_info($name="swdata");           
// foreach ($info as $i=>$column)
//     print_r($column->name +" "+ $column->type);

?>
