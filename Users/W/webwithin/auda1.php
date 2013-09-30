<?php
$html = scraperWiki::scrape("http://www.auda.org.au/domains/drop-list/");
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

scraperwiki::sqliteexecute("drop table if exists swdata"); 

$i=0;
foreach($dom->find("#purgedDroplist tr") as $data){
    if($i >= 1){
        $tds = $data->find("td");
        $record = array(
            "domain" => $tds[2]->plaintext,
            "date" => $tds[0]->plaintext,
            "time" => $tds[1]->plaintext
        );
        //print json_encode($record) . "\n";
        scraperwiki::save_sqlite(array("domain"), $record);
        //print_r($record).'\n';
        //echo $i.' ***************************************************************\n';
        
/*
        if($i > 5){
            echo $i.' ***************************************************************\n';
            break;
        }
*/
    }
    $i++;
}
?>
<?php
$html = scraperWiki::scrape("http://www.auda.org.au/domains/drop-list/");
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

scraperwiki::sqliteexecute("drop table if exists swdata"); 

$i=0;
foreach($dom->find("#purgedDroplist tr") as $data){
    if($i >= 1){
        $tds = $data->find("td");
        $record = array(
            "domain" => $tds[2]->plaintext,
            "date" => $tds[0]->plaintext,
            "time" => $tds[1]->plaintext
        );
        //print json_encode($record) . "\n";
        scraperwiki::save_sqlite(array("domain"), $record);
        //print_r($record).'\n';
        //echo $i.' ***************************************************************\n';
        
/*
        if($i > 5){
            echo $i.' ***************************************************************\n';
            break;
        }
*/
    }
    $i++;
}
?>
