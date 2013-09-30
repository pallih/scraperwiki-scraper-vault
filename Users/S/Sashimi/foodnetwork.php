<?php
# Blank PHP
require  'scraperwiki/simple_html_dom.php';

$myFood="maccheroni";
$foodNet="http://www.foodnetwork.com/search/delegate.do?fnSearchString=".$myFood."&fnSearchType=site";

$html = scraperwiki::scrape($foodNet);
getIngredients($html);

function getIngredients($html){
    $i=0;
    $dom = new simple_html_dom();
    $dom->load($html);
    //foreach($dom->find('result-item',1)->href as $data)
    //{  
       // if ($data != null)  
        //$res = trim($data->plaintext);
    $res=  $dom->find('a[class=callout]',1)->href;
 $res = str_replace("reviews/", "", $res);    
echo "http://www.foodnetwork.com".$res;
   
    $html1 = scraperwiki::scrape("http://www.foodnetwork.com".$res);
    $domFoods =  new simple_html_dom();
    //$domFoods->load($html1);
    $h = str_get_html($html1);
   //echo $domFoods;
   echo "\n\n";
foreach( $h->find('li[class=ingredient]') as $data){
    $ingredient = $data->plaintext;
    if(isset($h->href))  $href=$h->href;
    //foreach($domFoods->find('ul[class=kv-ingred-list1]',1)->children() as $data){
     //echo $data->plaintext;
    scraperwiki::save(array('ing'), array('ing' => $ingredient, 
                                            'href' =>$href));
    }


       
    
}


?>
<?php
# Blank PHP
require  'scraperwiki/simple_html_dom.php';

$myFood="maccheroni";
$foodNet="http://www.foodnetwork.com/search/delegate.do?fnSearchString=".$myFood."&fnSearchType=site";

$html = scraperwiki::scrape($foodNet);
getIngredients($html);

function getIngredients($html){
    $i=0;
    $dom = new simple_html_dom();
    $dom->load($html);
    //foreach($dom->find('result-item',1)->href as $data)
    //{  
       // if ($data != null)  
        //$res = trim($data->plaintext);
    $res=  $dom->find('a[class=callout]',1)->href;
 $res = str_replace("reviews/", "", $res);    
echo "http://www.foodnetwork.com".$res;
   
    $html1 = scraperwiki::scrape("http://www.foodnetwork.com".$res);
    $domFoods =  new simple_html_dom();
    //$domFoods->load($html1);
    $h = str_get_html($html1);
   //echo $domFoods;
   echo "\n\n";
foreach( $h->find('li[class=ingredient]') as $data){
    $ingredient = $data->plaintext;
    if(isset($h->href))  $href=$h->href;
    //foreach($domFoods->find('ul[class=kv-ingred-list1]',1)->children() as $data){
     //echo $data->plaintext;
    scraperwiki::save(array('ing'), array('ing' => $ingredient, 
                                            'href' =>$href));
    }


       
    
}


?>
