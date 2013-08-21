<?php
require 'scraperwiki/simple_html_dom.php';
scraperwiki::attach("xx_2", "src");
//scraperwiki::save_var('last_id', 120);
//exit(); 
$id= scraperwiki::get_var('last_id');
for($i=$id;$i<1000;$i++){
 $src = scraperwiki::select("* from src.swdata limit $i,1"); 
 $url = $src[0]['url'];
$url = str_replace('99tvshows.com/xx','baohanh.ninhkieumobile.com/demo/xx',$url);
 $html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);
$data = array();
$tr =  $html->find("form[name=delpost] div.maintable table tr.altbg1");
$j = 0;
foreach($tr as $trr){
$noidung = $trr->find('td table tr td span[style=font-size: 15px]',0)->innertext;
//$noidung = utf8_encode($noidung);
if(mb_strlen($noidung) >500){
    $j++;
  @scraperwiki::save_sqlite(array('id'),array('id'=> $j.'-'.$src[0]['url'], 'title'=>$src[0]['title'],'url'=> $src[0]['url'],'content'=>$noidung,'order'=> $j)); 
}
   
}
$html->clear();
unset($html);
scraperwiki::save_var('last_id', $i); 
}
?>
