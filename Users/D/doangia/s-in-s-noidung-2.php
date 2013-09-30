<?php
require 'scraperwiki/simple_html_dom.php';
scraperwiki::attach("s-in-s", "src");

//scraperwiki::save_var('last_id', 1);
//scraperwiki::save_var('my_id', 1);
//exit();
$id= scraperwiki::get_var('last_id');
$k= scraperwiki::get_var('my_id');
for($i=$id;$i<19000;$i++){
 $src = scraperwiki::select("* from src.swdata where type='nguoithe' limit $i,1");
 if(empty($src))
  break;
 $url = $src[0]['link'];

 $html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);
$data = array();
$tr =  $html->find("div.postmessage div.t_msgfont");
$j = 0;
foreach($tr as $trr){
$noidung = $trr->find('div',0)->innertext;
//$noidung = utf8_encode($noidung);
if(mb_strlen($noidung) >5000){
    $j++;
  @scraperwiki::save_sqlite(array('id'),array('id'=> 'mecon'.$k, 'title'=>$src[0]['title'],'url'=> $src[0]['url'],'content'=>base64_encode($noidung),'order'=> $j,'num'=>$src[0]['num'],'reply'=>$src[0]['reply'],'type'=>'nguoithe'));
    $k++;
scraperwiki::save_var('my_id', $k);
}
   
}
$html->clear();
unset($html);
scraperwiki::save_var('last_id', $i);
}
?><?php
require 'scraperwiki/simple_html_dom.php';
scraperwiki::attach("s-in-s", "src");

//scraperwiki::save_var('last_id', 1);
//scraperwiki::save_var('my_id', 1);
//exit();
$id= scraperwiki::get_var('last_id');
$k= scraperwiki::get_var('my_id');
for($i=$id;$i<19000;$i++){
 $src = scraperwiki::select("* from src.swdata where type='nguoithe' limit $i,1");
 if(empty($src))
  break;
 $url = $src[0]['link'];

 $html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);
$data = array();
$tr =  $html->find("div.postmessage div.t_msgfont");
$j = 0;
foreach($tr as $trr){
$noidung = $trr->find('div',0)->innertext;
//$noidung = utf8_encode($noidung);
if(mb_strlen($noidung) >5000){
    $j++;
  @scraperwiki::save_sqlite(array('id'),array('id'=> 'mecon'.$k, 'title'=>$src[0]['title'],'url'=> $src[0]['url'],'content'=>base64_encode($noidung),'order'=> $j,'num'=>$src[0]['num'],'reply'=>$src[0]['reply'],'type'=>'nguoithe'));
    $k++;
scraperwiki::save_var('my_id', $k);
}
   
}
$html->clear();
unset($html);
scraperwiki::save_var('last_id', $i);
}
?>