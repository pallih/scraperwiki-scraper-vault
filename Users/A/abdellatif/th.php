<?php

require 'scraperwiki/simple_html_dom.php';

$themes=array();

parseme("http://themeforest.net/category/all");

function parseme($link){
$html = file_get_html($link, false);
 
$lis=$html->find('ul.item-list li');

for($i=0;$i<count($lis);$i++){ 

$li= $lis[$i];

$images=$li->find('img[data-preview-url]');
$thumb=$images[0]->src; //-- 1
$themes[$i]['thumb']=$thumb;

$preview=$images[0]->attr['data-preview-url']; //-- 2
$themes[$i]['preview']=$preview;

$title=$images[0]->attr['data-item-name']; //-- 3
$themes[$i]['title']=$title;

$cost=$images[0]->attr['data-item-cost']; //-- 4
$themes[$i]['cost']=$cost;

$urls=$li->find('div.thumbnail a');
$url= "http://themeforest.net".$urls[0]->href; //-- 5
$themes[$i]['url']=$url;

$category=$images[0]->attr['data-item-category']; //-- 6
$themes[$i]['category']=$category;

$sales=  $li->find('small[class=sale-count]');
$sale = preg_replace("/[^\d|.]/", "", $sales[0]->innertext); //4
$themes[$i]['sale']=$sale;

$rating_img=  $li->find('div[class=rating] img');
$themes[$i]['rating']=count($rating_img);
}

# lets see if there's a next page
/* 
    if($next = $html->find('a[class=next_page]', 0)) {
        $nextURL = "http://themeforest.net".$next->href;
          echo $nextURL; 
       
        $html->clear();
        unset($html);
        
        parseme($nextURL);
    }
 
*/

print_r($themes);

}



?>
