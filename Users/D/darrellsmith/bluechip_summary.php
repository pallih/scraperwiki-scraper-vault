<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 848;
$i = 0;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

  while($i<=$maxpages){

    scraperwiki::save_var("page",$i);
    $url = "http://www.bluechipholidays.co.uk/holiday-cottages/results.html?limitstart=".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);
    // page
    foreach($dom->find('div[id=list_searchresults]') as $page){
      // cottage name and link
     foreach($page->find('div[class=hp_prop]') as $cottage){
  
       $cottage_Name = "";
       $cottage_URL = "";
    
       // name, ID and Link
       foreach($cottage->find('div[class=hp_title full]') as $details){
         foreach($details->find('h2') as $cottageURLData){
           $cottage_Name = strip_tags($cottageURLData); 
           foreach($cottageURLData->find('a') as $link){
              $cottage_URL = $link->href;
              
              $cot_id_Arr  = explode("|",$cottage_URL);
              $cottage_ID = $cot_id_Arr[1];
                
           }
         }
       }


       // Price 
       foreach($cottage->find('div[class=hp_price_wrap]') as $priceRange){
         foreach($priceRange->find('div[class=hp_price]') as $priceDetails){  
           $priceLow= str_replace("&pound;","",$priceDetails->plaintext);
         }
       }

       // features
       foreach($cottage->find('ul[class=hp_key_features]') as $data){
          foreach($data->find('li') as $feature){
             $features = $feature->plaintext.",";
           }
       }


       // sleeps, beds
       foreach($cottage->find('div[class=hp_extras]') as $priceRange){
         foreach($priceRange->find('span[class=rooms]') as $data){
           $sleeps = str_replace("","",$data->plaintext);
             foreach($data->find('strong') as $rooms){
               $bedrooms = $rooms->plaintext;
             } 
         }
         foreach($priceRange->find('span[class=sleeps]') as $data){
           foreach($data->find('strong') as $sleeps){
             $sleeps = $sleeps->plaintext;
           }
         }
       }
       
       
       

       $record = array(
        'COTTAGE_URL'   => "http://www.bluechipholidays.co.uk".$cottage_URL,
        'COTTAGE_NAME'  => $cottage_Name,
        'COTTAGE_ID'    => $cottage_ID,
        'SLEEPS'        => $sleeps,
        'BEDROOMS'      => $bedrooms,
        'FEATURES'      => $features,
        'PRICE_LOW'     => $priceLow,
       );      

       # print_r($record);
      scraperwiki::save(array('COTTAGE_URL'), $record);
}

// page and count
 
    }
   $i= $i+12;
  }
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 848;
$i = 0;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

  while($i<=$maxpages){

    scraperwiki::save_var("page",$i);
    $url = "http://www.bluechipholidays.co.uk/holiday-cottages/results.html?limitstart=".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);
    // page
    foreach($dom->find('div[id=list_searchresults]') as $page){
      // cottage name and link
     foreach($page->find('div[class=hp_prop]') as $cottage){
  
       $cottage_Name = "";
       $cottage_URL = "";
    
       // name, ID and Link
       foreach($cottage->find('div[class=hp_title full]') as $details){
         foreach($details->find('h2') as $cottageURLData){
           $cottage_Name = strip_tags($cottageURLData); 
           foreach($cottageURLData->find('a') as $link){
              $cottage_URL = $link->href;
              
              $cot_id_Arr  = explode("|",$cottage_URL);
              $cottage_ID = $cot_id_Arr[1];
                
           }
         }
       }


       // Price 
       foreach($cottage->find('div[class=hp_price_wrap]') as $priceRange){
         foreach($priceRange->find('div[class=hp_price]') as $priceDetails){  
           $priceLow= str_replace("&pound;","",$priceDetails->plaintext);
         }
       }

       // features
       foreach($cottage->find('ul[class=hp_key_features]') as $data){
          foreach($data->find('li') as $feature){
             $features = $feature->plaintext.",";
           }
       }


       // sleeps, beds
       foreach($cottage->find('div[class=hp_extras]') as $priceRange){
         foreach($priceRange->find('span[class=rooms]') as $data){
           $sleeps = str_replace("","",$data->plaintext);
             foreach($data->find('strong') as $rooms){
               $bedrooms = $rooms->plaintext;
             } 
         }
         foreach($priceRange->find('span[class=sleeps]') as $data){
           foreach($data->find('strong') as $sleeps){
             $sleeps = $sleeps->plaintext;
           }
         }
       }
       
       
       

       $record = array(
        'COTTAGE_URL'   => "http://www.bluechipholidays.co.uk".$cottage_URL,
        'COTTAGE_NAME'  => $cottage_Name,
        'COTTAGE_ID'    => $cottage_ID,
        'SLEEPS'        => $sleeps,
        'BEDROOMS'      => $bedrooms,
        'FEATURES'      => $features,
        'PRICE_LOW'     => $priceLow,
       );      

       # print_r($record);
      scraperwiki::save(array('COTTAGE_URL'), $record);
}

// page and count
 
    }
   $i= $i+12;
  }
?>
