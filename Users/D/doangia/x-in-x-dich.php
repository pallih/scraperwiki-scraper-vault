<?php
require 'scraperwiki/simple_html_dom.php';
//scraperwiki::save_var('last_id', 1303);
//exit();
$id= scraperwiki::get_var('last_id');
for($i=$id;$i<2600;$i++){
 $url = 'http://vietphrase.com/go/views.scraperwiki.com/run/x-in-x-view/?id='.$i;
 $html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);
$data = array();
 $title =  $html->find("div.title",0)->plaintext;
 $content =  $html->find("div.content",0)->innertext;
 $num =  $html->find("div.num",0)->plaintext;
 $reply =  $html->find("div.reply",0)->plaintext;
  $order =  $html->find("div.order",0)->plaintext;
 $url =  $html->find("div.url",0)->plaintext;
@scraperwiki::save_sqlite(array('id'),array('id'=> $order.'-'.$url, 'title'=>base64_encode($title),'url'=> $url,'content'=>base64_encode($content),'order'=> $order,'num'=>$num,'reply'=>$reply));
$html->clear();
unset($html);
scraperwiki::save_var('last_id', $i);
}
?>
<?php
require 'scraperwiki/simple_html_dom.php';
//scraperwiki::save_var('last_id', 1303);
//exit();
$id= scraperwiki::get_var('last_id');
for($i=$id;$i<2600;$i++){
 $url = 'http://vietphrase.com/go/views.scraperwiki.com/run/x-in-x-view/?id='.$i;
 $html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);
$data = array();
 $title =  $html->find("div.title",0)->plaintext;
 $content =  $html->find("div.content",0)->innertext;
 $num =  $html->find("div.num",0)->plaintext;
 $reply =  $html->find("div.reply",0)->plaintext;
  $order =  $html->find("div.order",0)->plaintext;
 $url =  $html->find("div.url",0)->plaintext;
@scraperwiki::save_sqlite(array('id'),array('id'=> $order.'-'.$url, 'title'=>base64_encode($title),'url'=> $url,'content'=>base64_encode($content),'order'=> $order,'num'=>$num,'reply'=>$reply));
$html->clear();
unset($html);
scraperwiki::save_var('last_id', $i);
}
?>
