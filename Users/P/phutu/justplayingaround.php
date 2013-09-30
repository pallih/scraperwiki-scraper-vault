<?php

# Blank PHP
$html = scraperWiki::scrape("http://reg.mcon-mannheim.de/onlineprogramm-mmv/render.aspx?kongressID=49&speach=&t=t&firstcall=1&z=634732416000000000");
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

//$firstRow = $dom->root->first_child()->children(1)->children(1)->children(0);
$secondRow = $dom->root->first_child()->children(1)->children(1)->children(1);

foreach($secondRow->find("td:first-child") as $data){
    $tds = $data->find("td");
    $record = array(
        'zeiten' => $tds->plaintext
    );
    print_r($record);
}
/*
foreach($firstRow->find("td") as $data){
    $ort = $data->plaintext;
    print_r($ort . "\n");
}
*/
/*
foreach($dom->find("td.tagesplanSitzung") as $data){
    $sitzung = $data->plaintext;
    print_r($sitzung . "\n");
}
*/
/*
foreach($dom->find("td.tagesplanSitzung") as $data){
    $record = array(
        'sitzung' => $data->plaintext
    );
    scraperwiki::save(array('sitzung'), $record);
}
*/
?>
<?php

# Blank PHP
$html = scraperWiki::scrape("http://reg.mcon-mannheim.de/onlineprogramm-mmv/render.aspx?kongressID=49&speach=&t=t&firstcall=1&z=634732416000000000");
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

//$firstRow = $dom->root->first_child()->children(1)->children(1)->children(0);
$secondRow = $dom->root->first_child()->children(1)->children(1)->children(1);

foreach($secondRow->find("td:first-child") as $data){
    $tds = $data->find("td");
    $record = array(
        'zeiten' => $tds->plaintext
    );
    print_r($record);
}
/*
foreach($firstRow->find("td") as $data){
    $ort = $data->plaintext;
    print_r($ort . "\n");
}
*/
/*
foreach($dom->find("td.tagesplanSitzung") as $data){
    $sitzung = $data->plaintext;
    print_r($sitzung . "\n");
}
*/
/*
foreach($dom->find("td.tagesplanSitzung") as $data){
    $record = array(
        'sitzung' => $data->plaintext
    );
    scraperwiki::save(array('sitzung'), $record);
}
*/
?>
