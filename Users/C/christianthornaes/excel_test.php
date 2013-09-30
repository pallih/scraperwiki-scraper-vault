<?php
require_once('scraperwiki/excel_reader2.php');  
         
$url = "http://www.whatdotheyknow.com/request/82804/response/208592/attach/2/ACCIDENTS%20TRAMS%20Laurderdale.xls";

file_put_contents("/tmp/spreadsheet.xls", scraperWiki::scrape($url));

$book = new Spreadsheet_Excel_Reader("/tmp/spreadsheet.xls");

print $book->rowcount() . "\n";
print $book->colcount() . "\n";

print $book->val(3, 1) . "\n";           
print $book->val(3, 'A') . "\n";

for ($col = 1; $col <= $book->colcount(); $col++) {           
    print $book->val(3, $col) . ",";
}

$keys = array('dummy');           
for ($col = 1; $col <= $book->colcount(); $col++) {
    $keys[] = str_replace(".", "", $book->val(3, $col));
}
print_r($keys);

for ($row = 1; $row <= $book->rowcount(); $row++) {           
    for ($col = 1; $col <= $book->colcount(); $col++) {
        if ($keys[$col]) {
            $data[$keys[$col]] = $book->val($row, $col);
        }
    }
    $data['rownumber'] = $row;

    print_r($data);

    if ($data['DATE'] != 'DATE' && $data['DATE'] && $data['FLEET NO']) {
        $data['DATE'] = DateTime::createFromFormat('d/m/y', $data['DATE'])->format('Y-m-d');
        scraperwiki::save(array('rownumber'), $data);
    }
}
?>
<?php
require_once('scraperwiki/excel_reader2.php');  
         
$url = "http://www.whatdotheyknow.com/request/82804/response/208592/attach/2/ACCIDENTS%20TRAMS%20Laurderdale.xls";

file_put_contents("/tmp/spreadsheet.xls", scraperWiki::scrape($url));

$book = new Spreadsheet_Excel_Reader("/tmp/spreadsheet.xls");

print $book->rowcount() . "\n";
print $book->colcount() . "\n";

print $book->val(3, 1) . "\n";           
print $book->val(3, 'A') . "\n";

for ($col = 1; $col <= $book->colcount(); $col++) {           
    print $book->val(3, $col) . ",";
}

$keys = array('dummy');           
for ($col = 1; $col <= $book->colcount(); $col++) {
    $keys[] = str_replace(".", "", $book->val(3, $col));
}
print_r($keys);

for ($row = 1; $row <= $book->rowcount(); $row++) {           
    for ($col = 1; $col <= $book->colcount(); $col++) {
        if ($keys[$col]) {
            $data[$keys[$col]] = $book->val($row, $col);
        }
    }
    $data['rownumber'] = $row;

    print_r($data);

    if ($data['DATE'] != 'DATE' && $data['DATE'] && $data['FLEET NO']) {
        $data['DATE'] = DateTime::createFromFormat('d/m/y', $data['DATE'])->format('Y-m-d');
        scraperwiki::save(array('rownumber'), $data);
    }
}
?>
