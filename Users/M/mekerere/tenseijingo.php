<?php
require 'scraperwiki/simple_html_dom.php';
date_default_timezone_set('Asia/Tokyo');
$html = file_get_html("http://www.asahi.com/paper/column.html");
#print $html;
$itemdate = $html->find('.LastUpdated', 0)->innertext;
$itemdate = mb_convert_encoding($itemdate,"UTF-8", "EUC-JP");
$data = $html->find("#MainInner p",1);
$data = mb_convert_encoding($data,"UTF-8", "EUC-JP");
$datestr = date("ymd");
#print $data;
scraperwiki::save(array("date"), array("date"=>$datestr, "text"=>$itemdate.$data)); 
$html->clear();
unset($html);
?>
