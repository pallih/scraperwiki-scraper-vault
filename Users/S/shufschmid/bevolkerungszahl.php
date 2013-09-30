<?php

require_once('scraperwiki/excel_reader2.php');
$url = "http://www.statistik-bs.ch/tabellen/t09/4/t09.4.03-12.xls";
file_put_contents("/tmp/spreadsheet.xls", scraperWiki::scrape($url));
$book = new Spreadsheet_Excel_Reader("/tmp/spreadsheet.xls");
print "hallo";
print $book->val(17, 'I') . "\n";           

?>
<?php

require_once('scraperwiki/excel_reader2.php');
$url = "http://www.statistik-bs.ch/tabellen/t09/4/t09.4.03-12.xls";
file_put_contents("/tmp/spreadsheet.xls", scraperWiki::scrape($url));
$book = new Spreadsheet_Excel_Reader("/tmp/spreadsheet.xls");
print "hallo";
print $book->val(17, 'I') . "\n";           

?>
