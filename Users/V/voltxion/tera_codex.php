<?php
$url = 'http://teracodex.com/item.php?type=';
$type_num = '2';
$html = scraperWiki::scrape($url . $type_num);       
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table.itemList tr") as $data){
    $tds = $data->find("td");
    //print_r($tds);
    $id = $data->find("td.tn a.codexToolTip");
    $record = array(
        'item_id' => $id[0]->attr['rel'],
        'type'=> intval($type_num),
        'name' => $tds[0]->plaintext, 
        'level' => intval($tds[1]->plaintext),
        'attack' => intval($tds[2]->plaintext),
        'extra_attack' => intval($tds[3]->plaintext),
        'obtained' => $tds[4]->plaintext,
        'eb' => $tds[5]->plaintext
    );
   scraperwiki::save(array(), $record,'tera_items');        
    
}
?>
