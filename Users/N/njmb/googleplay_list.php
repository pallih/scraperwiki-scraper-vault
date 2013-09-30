<?php
require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("https://play.google.com/store/apps?feature=corpus_selector");
$html = str_get_html($html_content);

//"collection/topselling_paid?start=24&num=24"
//topselling_free

//データ削除
scraperwiki::sqliteexecute("drop table swdata");
scraperwiki::sqlitecommit();  


foreach ($html->find("li.category-item a") as $el) { 

    //ゴミは無視
    if($el->find(".more-arrow")){
        continue;
    }
    
    //print($el->innertext). "\n";
    
    $temp = array("0"=>"topselling_free","1"=>"topselling_paid");
    
    foreach($temp as $key =>$str){
        for($i=0;$i<5*24;$i=$i+24){
             $record = array(
            'link'=>"https://play.google.com".str_replace("?feature=category-nav","",$el->href)."/collection/".$str."?start=".$i."&num=24",
            'category'=>$el->innertext,
             'paid'=>$key,
            'startRank'=>$i);
    
    
        //print json_encode($record) . "\n";
        scraperwiki::save(array('category','link','paid','link','startRank'), $record); 
        }
    }

}
?><?php
require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("https://play.google.com/store/apps?feature=corpus_selector");
$html = str_get_html($html_content);

//"collection/topselling_paid?start=24&num=24"
//topselling_free

//データ削除
scraperwiki::sqliteexecute("drop table swdata");
scraperwiki::sqlitecommit();  


foreach ($html->find("li.category-item a") as $el) { 

    //ゴミは無視
    if($el->find(".more-arrow")){
        continue;
    }
    
    //print($el->innertext). "\n";
    
    $temp = array("0"=>"topselling_free","1"=>"topselling_paid");
    
    foreach($temp as $key =>$str){
        for($i=0;$i<5*24;$i=$i+24){
             $record = array(
            'link'=>"https://play.google.com".str_replace("?feature=category-nav","",$el->href)."/collection/".$str."?start=".$i."&num=24",
            'category'=>$el->innertext,
             'paid'=>$key,
            'startRank'=>$i);
    
    
        //print json_encode($record) . "\n";
        scraperwiki::save(array('category','link','paid','link','startRank'), $record); 
        }
    }

}
?>