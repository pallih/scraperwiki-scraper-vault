<?php
require 'scraperwiki/simple_html_dom.php';
for($i=1;$i<56;$i++){
$html_content = scraperwiki::scrape("http://vietphrase.com/go/sexinsex.net/bbs/forumdisplay.php?fid=110&filter=type&typeid=294&page=$i");

$html = str_get_html($html_content);
$data = array();
foreach($html->find('table#forum_110 tbody[id]') as $tbody)
{
 
 
    $link = $title = $num = "";
    foreach($tbody->find('tr th.hot') as $th){
    //echo  $th->innnertext;
    //exit();
       $link = $th->find('span',0)->find('a',0)->href;
       $title = $th->find('span',0)->find('a',0)->plaintext;    
          $num = $th->parent()->find('td.nums em',0)->plaintext;    
           $reply = $th->parent()->find('td.nums strong',0)->plaintext; 
//exit();
     scraperwiki::save_sqlite(array('url'),array('title'=>base64_encode($title),'url'=> base64_encode($link),'link'=>$link,'num'=>$num,'reply'=>$reply,'type'=>'nguoithe'));
    }

   
 //scraperwiki::save_sqlite(array('url'),array('title'=>$a->plaintext,'url'=> $a->href,'ok'=>0));
//break;
}
$html->clear();
unset($html);
}


?>