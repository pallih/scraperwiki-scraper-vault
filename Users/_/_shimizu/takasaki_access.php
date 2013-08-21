<?php
require 'scraperwiki/simple_html_dom.php';      
mb_language('Japanese');

$url = 'http://www.city.takasaki.gunma.jp/gaiyou/access.htm';
$contents = file_get_contents($url);
$content = mb_convert_encoding($contents, 'UTF-8', 'auto');
$html = str_get_html($content);


$record = array();
$tmp = array();
$id = 0;
foreach($html->find('table#honbun > tbody > tr > td > table >tbody > tr') as $tr){
       $ths = $tr->find('th');
       $tds =  $tr->find('td');
       
       for($i=0;$i < count($ths); $i++){
            $tmp['id'] = $id;
            $tmp['name'] = $ths[$i]->text();
            $tmp['line'] = $tds[0]->text();
            $str = $tds[1]->text();
            $tmp['km'] =  str_replace( 'キロメートル', '', $str);
            $tmp['time'] =  $tds[2]->text();
            
            array_push($record, $tmp);
            $id++;
       }

}

print json_encode($record). "\n";
scraperwiki::save(array('id'), $record);

?>
