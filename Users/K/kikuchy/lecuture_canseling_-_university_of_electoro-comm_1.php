<?php

$html = mb_convert_encoding(scraperWiki::scrape("http://kyoumu.office.uec.ac.jp/kyuukou/kyuukou.html"),
            "UTF-8", "SJIS");
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$trs = $dom->find("table tr");
for($i = 1; $i < count($trs); $i++){
    $tr = $trs[$i];
    $tds = $tr->find("td");
    $record = array(
        "class" => $tds[0]->plaintext,
        "date" => $tds[1]->plaintext,
        "period" => intval($tds[2]->plaintext),
        "subject" => $tds[3]->plaintext,
        "teacher" => $tds[4]->plaintext,
        "note" => $tds[5]->plaintext
    );
    print $tds[5]->plaintext . "\n";
    scraperwiki::save(array('date'), $record);  
}


?>
