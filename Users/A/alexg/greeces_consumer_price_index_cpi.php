<?php

/* scraper by Alex Georgiou http://www.alexgeorgiou.gr */

require 'scraperwiki/simple_html_dom.php';

scraperwiki::sqliteexecute("create table if not exists cpi (month date, value decimal)"); 

$url = "http://www.dsalib.gr/popups/dkt.html";
$html = scraperwiki::scrape($url);
$dom = new simple_html_dom();
$dom->load($html);


$data = array();

$row_num=0;
foreach ($dom->find('table.MsoTableContemporary tr') as $row) {
    if ($row_num>0) {
        $col_num = 0;
        foreach($row->find('td') as $cell) {
            if ($col_num>0) {

                //time
                $year = $col_num +2000;
                $month = $row_num;
                if ($month<10) $month = "0$month";
                $date = "$year-$month-01";

                //value
                $matches = array();
                if (preg_match("/(\d{1,2}),(\d)\%/",$cell->plaintext,$matches)) {
                    $value = "$matches[1].$matches[2]";
    
                    //echo "$row_num  ,  $col_num  ,  $cell->plaintext , $value \n";
                    $data[] = array(
                        'month' => $date,
                        'value' => $value
                    );
                }
            }
            $col_num++;
        }
    }
    $row_num++;
}
scraperwiki::save_sqlite(array('month'),$data, "cpi");
?><?php

/* scraper by Alex Georgiou http://www.alexgeorgiou.gr */

require 'scraperwiki/simple_html_dom.php';

scraperwiki::sqliteexecute("create table if not exists cpi (month date, value decimal)"); 

$url = "http://www.dsalib.gr/popups/dkt.html";
$html = scraperwiki::scrape($url);
$dom = new simple_html_dom();
$dom->load($html);


$data = array();

$row_num=0;
foreach ($dom->find('table.MsoTableContemporary tr') as $row) {
    if ($row_num>0) {
        $col_num = 0;
        foreach($row->find('td') as $cell) {
            if ($col_num>0) {

                //time
                $year = $col_num +2000;
                $month = $row_num;
                if ($month<10) $month = "0$month";
                $date = "$year-$month-01";

                //value
                $matches = array();
                if (preg_match("/(\d{1,2}),(\d)\%/",$cell->plaintext,$matches)) {
                    $value = "$matches[1].$matches[2]";
    
                    //echo "$row_num  ,  $col_num  ,  $cell->plaintext , $value \n";
                    $data[] = array(
                        'month' => $date,
                        'value' => $value
                    );
                }
            }
            $col_num++;
        }
    }
    $row_num++;
}
scraperwiki::save_sqlite(array('month'),$data, "cpi");
?>