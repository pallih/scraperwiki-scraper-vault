<?php


require 'scraperwiki/simple_html_dom.php';      
mb_language('Japanese');

$url = 'http://www.ethnologue.com/statistics/size';

$contents = file_get_contents($url);
$content = mb_convert_encoding($contents, 'UTF-8', 'auto');
$html = str_get_html($content);


$record = array();
$tmp = array();

$table = $html->find('.statistical', 1);
$trs = $table->find('tr');
for($i=1; $i < count($trs); $i++){
    $tds = $trs[$i]->find('td');
    $rank = str_replace("&nbsp;", "",  trim($tds[0]->text()) );
    if(empty($rank)) continue;
    $tmp['rank'] =  $rank;
    $tmp['language'] =  $tds[1]->text();
    $tmp['primary_country'] =  $tds[2]->text();
    $tmp['total_countries'] = $tds[3]->text();
    $tmp['speakers_millions'] = $tds[4]->text();    
    array_push($record, $tmp);
}


print json_encode($record). "\n";
scraperwiki::save(array('rank'), $record);


?>
<?php


require 'scraperwiki/simple_html_dom.php';      
mb_language('Japanese');

$url = 'http://www.ethnologue.com/statistics/size';

$contents = file_get_contents($url);
$content = mb_convert_encoding($contents, 'UTF-8', 'auto');
$html = str_get_html($content);


$record = array();
$tmp = array();

$table = $html->find('.statistical', 1);
$trs = $table->find('tr');
for($i=1; $i < count($trs); $i++){
    $tds = $trs[$i]->find('td');
    $rank = str_replace("&nbsp;", "",  trim($tds[0]->text()) );
    if(empty($rank)) continue;
    $tmp['rank'] =  $rank;
    $tmp['language'] =  $tds[1]->text();
    $tmp['primary_country'] =  $tds[2]->text();
    $tmp['total_countries'] = $tds[3]->text();
    $tmp['speakers_millions'] = $tds[4]->text();    
    array_push($record, $tmp);
}


print json_encode($record). "\n";
scraperwiki::save(array('rank'), $record);


?>
