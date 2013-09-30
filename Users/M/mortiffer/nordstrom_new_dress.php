<?php

# Blank PHP
$html = scraperWiki::scrape("http://shop.nordstrom.com/c/womens-clothing-new/dresses#category=b6007338%7Cf8000802&type=category&marketingslots=2&currency=CHF&page=1&size=&width=&color=&price=&brand=&instoreavailability=false&lastfilter=&sizeFinderId=2&resultsmode=&segmentId=0&sort=newest&sortreverse=0");    

$url_page2_all="http://shop.nordstrom.com/c/womens-clothing-new?origin=leftnav#category=b6007338&type=category&marketingslots=2&currency=CHF&page=1&size=&width=&color=&price=&brand=&instoreavailability=false&lastfilter=&sizeFinderId=2&resultsmode=&segmentId=0&sort=newest&sortreverse=0";

$html_allClothing=scraperWiki::scrape($url_page2_all);

$html_bigLimit= scraperWiki::scrape("http://shop.nordstrom.com/c/womens-clothing-new/dresses#category=b6007338%7Cf8000802&type=category&marketingslots=2&currency=CHF&page=2&instoreavailability=false&sizeFinderId=2&segmentId=0&sort=newest&sortreverse=0&partial=0&pagesize=1000&contextualsortcategoryid=0");
 

 //print($html);
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html_allClothing);
//print($html);
$count = 1;
$maxDataInserts = 5000;
foreach($dom->find('div[class="fashion-item"],div[class="fashion-item first"]') as $data){
  
    if($count>$maxDataInserts){
        break;
    }
    $count = $count+1;
 //print($data);
    $id = $data->getAttribute('id');
    $picURL = $data->find("img", 0);
    $title = $data->find('a[class="title"]');
    $price = $data->find('span[class="price regular"]');
    
     //print_r($id[0]->plaintext);
    // print_r($price[0]->plaintext);  //works 
    // print_r($title[0]->plaintext);//works 

  //  print_r($picURL->getAttribute('data-original'));


echo ('>>');
    if(count($price)>0){
        $record = array(
        
            'id' => $id, 
            'picUrl_small' => $picURL->getAttribute('data-original'),
            'price' => $price[0]->plaintext,
            'title' =>$title[0]->plaintext
        );
        scraperwiki::save(array('id','picUrl_small','price','title'), $record); 
echo ('<|savedrecord|>');
    }
}
echo ('<DONE>');
?>
<?php

# Blank PHP
$html = scraperWiki::scrape("http://shop.nordstrom.com/c/womens-clothing-new/dresses#category=b6007338%7Cf8000802&type=category&marketingslots=2&currency=CHF&page=1&size=&width=&color=&price=&brand=&instoreavailability=false&lastfilter=&sizeFinderId=2&resultsmode=&segmentId=0&sort=newest&sortreverse=0");    

$url_page2_all="http://shop.nordstrom.com/c/womens-clothing-new?origin=leftnav#category=b6007338&type=category&marketingslots=2&currency=CHF&page=1&size=&width=&color=&price=&brand=&instoreavailability=false&lastfilter=&sizeFinderId=2&resultsmode=&segmentId=0&sort=newest&sortreverse=0";

$html_allClothing=scraperWiki::scrape($url_page2_all);

$html_bigLimit= scraperWiki::scrape("http://shop.nordstrom.com/c/womens-clothing-new/dresses#category=b6007338%7Cf8000802&type=category&marketingslots=2&currency=CHF&page=2&instoreavailability=false&sizeFinderId=2&segmentId=0&sort=newest&sortreverse=0&partial=0&pagesize=1000&contextualsortcategoryid=0");
 

 //print($html);
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html_allClothing);
//print($html);
$count = 1;
$maxDataInserts = 5000;
foreach($dom->find('div[class="fashion-item"],div[class="fashion-item first"]') as $data){
  
    if($count>$maxDataInserts){
        break;
    }
    $count = $count+1;
 //print($data);
    $id = $data->getAttribute('id');
    $picURL = $data->find("img", 0);
    $title = $data->find('a[class="title"]');
    $price = $data->find('span[class="price regular"]');
    
     //print_r($id[0]->plaintext);
    // print_r($price[0]->plaintext);  //works 
    // print_r($title[0]->plaintext);//works 

  //  print_r($picURL->getAttribute('data-original'));


echo ('>>');
    if(count($price)>0){
        $record = array(
        
            'id' => $id, 
            'picUrl_small' => $picURL->getAttribute('data-original'),
            'price' => $price[0]->plaintext,
            'title' =>$title[0]->plaintext
        );
        scraperwiki::save(array('id','picUrl_small','price','title'), $record); 
echo ('<|savedrecord|>');
    }
}
echo ('<DONE>');
?>
