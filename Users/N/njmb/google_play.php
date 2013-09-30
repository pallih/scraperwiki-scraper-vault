<?php
//ランク取得
require 'scraperwiki/simple_html_dom.php'; 

//データ削除
scraperwiki::sqliteexecute("drop table swdata");
scraperwiki::sqlitecommit();  

//とりあえず、limit 10
$detailListHtml = scraperwiki::scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=googleplay_list&query=select%20*%20from%20%60swdata%60%20limit%2010");
        

$objData  = json_decode($detailListHtml);

//var_dump($objData);

foreach($objData as $item){

    $html_content = scraperwiki::scrape($item->link);
    $html = str_get_html($html_content);
    
    $i=$item->startRank+1;
    foreach ($html->find("a.title") as $el) { 
    
    
         $record = array(
                        'rank'=>$i,
                        'title'=>$el->title,
                        'link'=>"https://play.google.com".$el->href,
                        'date'=>date('Y-m-d'));
        
        //print json_encode($record) . "\n";
        scraperwiki::save(array('rank','title','link','date'), $record); 
        $i++; 
    }
}
?>
<?php
//ランク取得
require 'scraperwiki/simple_html_dom.php'; 

//データ削除
scraperwiki::sqliteexecute("drop table swdata");
scraperwiki::sqlitecommit();  

//とりあえず、limit 10
$detailListHtml = scraperwiki::scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=googleplay_list&query=select%20*%20from%20%60swdata%60%20limit%2010");
        

$objData  = json_decode($detailListHtml);

//var_dump($objData);

foreach($objData as $item){

    $html_content = scraperwiki::scrape($item->link);
    $html = str_get_html($html_content);
    
    $i=$item->startRank+1;
    foreach ($html->find("a.title") as $el) { 
    
    
         $record = array(
                        'rank'=>$i,
                        'title'=>$el->title,
                        'link'=>"https://play.google.com".$el->href,
                        'date'=>date('Y-m-d'));
        
        //print json_encode($record) . "\n";
        scraperwiki::save(array('rank','title','link','date'), $record); 
        $i++; 
    }
}
?>
