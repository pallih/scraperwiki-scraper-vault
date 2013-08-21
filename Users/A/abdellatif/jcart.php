<?php

require 'scraperwiki/simple_html_dom.php';

 
 

function scraping_jumia($link,$cat,$provider) {
  

 
  $insert_arr=array();

 $html = file_get_html($link, false);
 
 $lis=$html->find('#productsCatalog li');

if(count($lis) >0){

for($i=0;$i<count($lis);$i++){ 
 
$li= $lis[$i];//0,1,2,3
 
 //-- for thumbe 
$images=$li->find('img.itm-img'); //itm-img loading // itm-img  
$dflt_thumb= $images[0]->src; //--- 1
//echo $dflt_thumb."<br>"; 
$insert_arr[0]=$dflt_thumb;

//  title + link
$atext= $li->find('em.itm-title');//itm-listview-title //itm-title
$title=$atext[0]->plaintext; // 2
//echo $title."<br>";
$insert_arr[1]=$title;

$alink= $li->find('a');
$p_link= "https://www.jumia.com.eg".$alink[0]->href."?lang=ar_EG";// 3
//echo $p_link."<br>";
$insert_arr[2]=$p_link;

//original_price
$price=  $li->find('span[class=itm-price old]');
 
$original_price = preg_replace("/[^\d|.]/", "", $price[0]->innertext); //4
//echo $original_price."<br>"; 

$insert_arr[3]=$original_price;

//Price
$td3=  $li->find('span[class=itm-price special]'); //itm-price special bold //itm-price special
$price  = preg_replace("/[^\d|.]/", "", $td3[0]->innertext);  // 7
//echo $price."<br>"; 
$insert_arr[4]=$price;
/*
//$describe
$td4=  $li->find('div[class=shortListViewShortDescription]'); //itm-price special bold //itm-price special
$describe  = $td4[0]->innertext;  // 7
echo $describe."<br>"; 
*/
$insert_arr[5]=$cat;
$insert_arr[6]=$provider;

save_data($insert_arr);
 
}



}



 $html->clear();
  unset($html);

 
 
 

}
function save_data($arr){
        $data = array
                    (
                        'item_photo' => $arr[0],
                        'item_name' => $arr[1],
                        'item_source' => $arr[2],
                        'item_original_price' =>  $arr[3],
                        'item_price' =>  $arr[4],
                        'item_rate' => ceil((($arr[3]-$arr[4])/$arr[3])*100),
                        'item_cat_id' => $arr[5],
                        'item_provider' => $arr[6],
                        
                         
                    );

 scraperwiki::save(array('item_name'), $data);
}

function delete_by_cat($cat,$provider){
scraperwiki::sqliteexecute("delete from swdata where item_cat_id=$cat and item_provider=$provider"); 
}
 


delete_by_cat(1,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/fashion-by-jumia/?lang=ar_EG&page='.$i,1,1); 
         }


delete_by_cat(2,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/mobiles-accessories/?lang=ar_EG&page='.$i,2,1); 
         }


delete_by_cat(3,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/electronics-computers/?lang=ar_EG&page='.$i,3,1); 
         }


delete_by_cat(4,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/audio-video/?lang=ar_EG&page='.$i,4,1); 
         }


delete_by_cat(5,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/cameras-and-recorders/?lang=ar_EG&page='.$i,5,1); 
         }

delete_by_cat(6,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/home-kitchen-appliances/?lang=ar_EG&page='.$i,6,1); 
         }


delete_by_cat(7,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/fragrances/?lang=ar_EG&page='.$i,7,1); 
         }


delete_by_cat(8,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/watches/?lang=ar_EG&page='.$i,8,1); 
         }


delete_by_cat(9,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/gaming/?lang=ar_EG&page='.$i,9,1); 
         }


delete_by_cat(10,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/health-beauty/?lang=ar_EG&page='.$i,10,1); 
         }

delete_by_cat(11,1);
for ($i = 1; $i < 6; $i++) {
             scraping_jumia('https://www.jumia.com.eg/special-price/kids-toys/?lang=ar_EG&page='.$i,11,1); 
         }

 


?>
