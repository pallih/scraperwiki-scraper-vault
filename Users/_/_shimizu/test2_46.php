<?php

require 'scraperwiki/simple_html_dom.php';      
mb_language('Japanese');

$url = 'http://www.teiocollection.com/kakaku.htm';
$contents = file_get_contents($url);
$content = mb_convert_encoding($contents, 'UTF-8', 'auto');
$html = str_get_html($content);


$record = array();
$tmp = array();

$table = $html->find('table', 2);
$trs = $table->find('tr');
for($i=1; $i < count($trs); $i++){
    $tds = $trs[$i]->find('td');
    $tmp['id'] = $tds[0]->text();
    $tmp['item'] =  $tds[1]->text();
    $tmp['quality'] =  $tds[2]->text();
    $tmp['edo_price'] = $tds[3]->text();
    $tmp['price'] = $tds[4]->text();
    array_push($record, $tmp);
}

print json_encode($record). "\n";
scraperwiki::save(array('id'), $record);


?>
<?php

require 'scraperwiki/simple_html_dom.php';      
mb_language('Japanese');

$url = 'http://www.teiocollection.com/kakaku.htm';
$contents = file_get_contents($url);
$content = mb_convert_encoding($contents, 'UTF-8', 'auto');
$html = str_get_html($content);


$record = array();
$tmp = array();

$table = $html->find('table', 2);
$trs = $table->find('tr');
for($i=1; $i < count($trs); $i++){
    $tds = $trs[$i]->find('td');
    $tmp['id'] = $tds[0]->text();
    $tmp['item'] =  $tds[1]->text();
    $tmp['quality'] =  $tds[2]->text();
    $tmp['edo_price'] = $tds[3]->text();
    $tmp['price'] = $tds[4]->text();
    array_push($record, $tmp);
}

print json_encode($record). "\n";
scraperwiki::save(array('id'), $record);


?>
