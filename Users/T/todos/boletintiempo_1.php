<?php

$html = scraperWiki::scrape("http://www.insivumeh.gob.gt/meteorologia/boletintiempo.htm");
//print $html . "\n";
scraperwiki::sqliteexecute("drop table if exists ciudad"); 

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table tr[@align='center']") as $data){
    $tds = $data->find("td");
    $record = array(
        'ciudad' => $tds[0]->plaintext, 
        'direccion del viento' => $tds[1]->plaintext, 
        'viento km/h' => intval($tds[2]->plaintext),
        'visibilidad' => $tds[3]->plaintext, 
        'tiempo presente' => $tds[4]->plaintext,
        'nubosidad' => $tds[5]->plaintext,
        'temperatura' => $tds[7]->plaintext,  
        'humedad relativa' => $tds[8]->plaintext, 
        'hora' => $tds[9]->plaintext, 
    );
   print_r($record);
   scraperwiki::save(array('ciudad'), $record);


}

?>

<?php

$html = scraperWiki::scrape("http://www.insivumeh.gob.gt/meteorologia/boletintiempo.htm");
//print $html . "\n";
scraperwiki::sqliteexecute("drop table if exists ciudad"); 

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table tr[@align='center']") as $data){
    $tds = $data->find("td");
    $record = array(
        'ciudad' => $tds[0]->plaintext, 
        'direccion del viento' => $tds[1]->plaintext, 
        'viento km/h' => intval($tds[2]->plaintext),
        'visibilidad' => $tds[3]->plaintext, 
        'tiempo presente' => $tds[4]->plaintext,
        'nubosidad' => $tds[5]->plaintext,
        'temperatura' => $tds[7]->plaintext,  
        'humedad relativa' => $tds[8]->plaintext, 
        'hora' => $tds[9]->plaintext, 
    );
   print_r($record);
   scraperwiki::save(array('ciudad'), $record);


}

?>

