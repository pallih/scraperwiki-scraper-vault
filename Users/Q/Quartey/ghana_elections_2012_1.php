<?php
require_once('scraperwiki/excel_reader2.php');
$url = "http://www.ec.gov.gh/page.php?page=469&section=49&typ=1";
file_put_contents("/tmp/spreadsheet.xls", scraperWiki::scrape($url));
$book = new Spreadsheet_Excel_Reader("/tmp/spreadsheet.xls");
print $book->rowcount() . "\n";
print $book->colcount() . "\n";
?>
