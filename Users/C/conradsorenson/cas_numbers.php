<?php

//    1  Create database
require 'scraperwiki/simple_html_dom.php';    

$surl = "https://www.enabling-materials.com/CAS_Numbers.txt";

$CAS_Numbers = scraperwiki::scrape($surl);


$CAS_Numbers_dom = new simple_html_dom();
$CAS_Numbers_dom->load($CAS_Numbers);

//echo $CAS_Numbers_dom;
//echo trim($CAS_Numbers_dom->plaintext);
$CAN_Numbers_List=trim($CAS_Numbers_dom->plaintext);

// Break into pieces
$pieces = explode(",", $CAN_Numbers_List);
//echo $pieces[0] . "\n"; // piece1
//echo $pieces[1] . "\n"; // piece2


scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `CAS_Numbers` ('Index' number, `Number` text)");

$intCount = 1;
foreach($pieces as $data){
    //echo $data . "\n";

    $record = array(
        'Index' => $intCount,
        'Number' => $data
    );
    //scraperwiki::save_sqlite(array('CAS_Number'), $record);
    scraperwiki::save_sqlite(array('Number'), $record, "CAS_Numbers", 1);
    $intCount++;

    
}

?>
