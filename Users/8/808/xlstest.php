<?php

set_time_limit(0);

require 'scraperwiki/simple_html_dom.php';

require_once('scraperwiki/excel_reader2.php');
$url = "http://dev.dynamicdataware.com/scraper/1_INHSsources_0-65535.xls";
file_put_contents("/tmp/spreadsheet.xls", scraperWiki::scrape($url));
$book = new Spreadsheet_Excel_Reader("/tmp/spreadsheet.xls");

print $book->rowcount() . "\n";           
print $book->colcount() . "\n";

for ($row = 1; $row <= $book->rowcount(); $row++) {           
    print $book->val($row, 1) . "\n";
}

?>
