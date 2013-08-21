<?php

# Blank PHP

// scraperwiki::sqliteexecute("create table reg_no (reg_no string, unique(reg_no))");

// scraperwiki::sqliteexecute("delete from reg_no where reg_no LIKE '%AP09AD%'");
// scraperwiki::sqlitecommit();           


$data = scraperWiki::scrape('http://dl.dropbox.com/u/36789/ash/ap09acad.csv');     
 
$lines = explode("\n", $data);           

foreach($lines as $row) {           
    $row = str_getcsv($row);
    $v_reg_no = $row[0];
    printf("Vehicle No: %s\n", $v_reg_no);
    scraperwiki::sqliteexecute("insert or replace into reg_no values (:reg_no)", array("reg_no"=>$v_reg_no));
}     

scraperwiki::sqlitecommit();           

?>
