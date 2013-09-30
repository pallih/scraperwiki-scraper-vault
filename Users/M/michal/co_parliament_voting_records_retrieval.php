<?php
//


require_once('scraperwiki/excel_reader2.php');

//read the saved tables
scraperwiki::attach("co_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("* from src.file");

$handle = fopen('/tmp/co_parl.xls',"w+");
echo count($rows[3]);
fwrite($handle,base64_decode($rows[3]['file_blob']));

$book = new Spreadsheet_Excel_Reader("/tmp/co_parl.xls");

print $book->rowcount() . "\n";
print $book->colcount() . "\n";

print $book->val(1, 1) ."\n";

?>
<?php
//


require_once('scraperwiki/excel_reader2.php');

//read the saved tables
scraperwiki::attach("co_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("* from src.file");

$handle = fopen('/tmp/co_parl.xls',"w+");
echo count($rows[3]);
fwrite($handle,base64_decode($rows[3]['file_blob']));

$book = new Spreadsheet_Excel_Reader("/tmp/co_parl.xls");

print $book->rowcount() . "\n";
print $book->colcount() . "\n";

print $book->val(1, 1) ."\n";

?>
<?php
//


require_once('scraperwiki/excel_reader2.php');

//read the saved tables
scraperwiki::attach("co_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("* from src.file");

$handle = fopen('/tmp/co_parl.xls',"w+");
echo count($rows[3]);
fwrite($handle,base64_decode($rows[3]['file_blob']));

$book = new Spreadsheet_Excel_Reader("/tmp/co_parl.xls");

print $book->rowcount() . "\n";
print $book->colcount() . "\n";

print $book->val(1, 1) ."\n";

?>
<?php
//


require_once('scraperwiki/excel_reader2.php');

//read the saved tables
scraperwiki::attach("co_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("* from src.file");

$handle = fopen('/tmp/co_parl.xls',"w+");
echo count($rows[3]);
fwrite($handle,base64_decode($rows[3]['file_blob']));

$book = new Spreadsheet_Excel_Reader("/tmp/co_parl.xls");

print $book->rowcount() . "\n";
print $book->colcount() . "\n";

print $book->val(1, 1) ."\n";

?>
