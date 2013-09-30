<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 37;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.suffolk-secrets.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=search-container]') as $page){
      // cottage

      foreach($page->find('div[class=property_result]') as $cottage){
        $cottage_name = "";
        foreach($cottage->find('div[class=property_right]') as $details){

             # cottage name, URL and ID
             foreach($details->find('h2') as $cottageNameData){
               foreach($details->find('a') as $cottageURLData){
                 if($cottage_name == "")   
                   $cottage_name = $cottageURLData->plaintext;     
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }

             foreach($details->find('span[class=price]') as $priceData){
                 $priceLow = str_replace("&pound;","",$priceData->plaintext);
             }


             # cottage Pets, Bedrooms and Sleeps
             foreach($details->find('div[class=details]') as $cottagefeatures){
               foreach($details->find('ul') as $list){
                 $listArr = explode(":",str_replace("&nbsp;","",$list->plaintext));            
                 if(strpos($listArr[2],"Yes"))
                    $pets = 1;
                   else $pets = 0;
                 $bedrooms = str_replace("Internet","",$listArr[3]);
                 $sleeps = str_replace("Pets","",$listArr[1]);
                 $changeover = $listArr[6];
             }
        }

        
 
        $record = array(
          'COTTAGE_URL'   => "http://www.suffolk-secrets.co.uk".$cottage_URL,
          'COTTAGE_NAME'  => $cottage_name,
          'COTTAGE_ID'    => $cottage_ID,
          'SLEEPS'        => $sleeps,
          'BEDROOMS'      => $bedrooms,
          'PETS'          => $pets,
          'PRICE_LOW'     => $priceLow,
        );   
 
       
        scraperwiki::save(array('COTTAGE_URL'), $record);


      }
    }
}
 $i++;

}
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 37;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.suffolk-secrets.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=search-container]') as $page){
      // cottage

      foreach($page->find('div[class=property_result]') as $cottage){
        $cottage_name = "";
        foreach($cottage->find('div[class=property_right]') as $details){

             # cottage name, URL and ID
             foreach($details->find('h2') as $cottageNameData){
               foreach($details->find('a') as $cottageURLData){
                 if($cottage_name == "")   
                   $cottage_name = $cottageURLData->plaintext;     
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }

             foreach($details->find('span[class=price]') as $priceData){
                 $priceLow = str_replace("&pound;","",$priceData->plaintext);
             }


             # cottage Pets, Bedrooms and Sleeps
             foreach($details->find('div[class=details]') as $cottagefeatures){
               foreach($details->find('ul') as $list){
                 $listArr = explode(":",str_replace("&nbsp;","",$list->plaintext));            
                 if(strpos($listArr[2],"Yes"))
                    $pets = 1;
                   else $pets = 0;
                 $bedrooms = str_replace("Internet","",$listArr[3]);
                 $sleeps = str_replace("Pets","",$listArr[1]);
                 $changeover = $listArr[6];
             }
        }

        
 
        $record = array(
          'COTTAGE_URL'   => "http://www.suffolk-secrets.co.uk".$cottage_URL,
          'COTTAGE_NAME'  => $cottage_name,
          'COTTAGE_ID'    => $cottage_ID,
          'SLEEPS'        => $sleeps,
          'BEDROOMS'      => $bedrooms,
          'PETS'          => $pets,
          'PRICE_LOW'     => $priceLow,
        );   
 
       
        scraperwiki::save(array('COTTAGE_URL'), $record);


      }
    }
}
 $i++;

}
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 37;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.suffolk-secrets.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=search-container]') as $page){
      // cottage

      foreach($page->find('div[class=property_result]') as $cottage){
        $cottage_name = "";
        foreach($cottage->find('div[class=property_right]') as $details){

             # cottage name, URL and ID
             foreach($details->find('h2') as $cottageNameData){
               foreach($details->find('a') as $cottageURLData){
                 if($cottage_name == "")   
                   $cottage_name = $cottageURLData->plaintext;     
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }

             foreach($details->find('span[class=price]') as $priceData){
                 $priceLow = str_replace("&pound;","",$priceData->plaintext);
             }


             # cottage Pets, Bedrooms and Sleeps
             foreach($details->find('div[class=details]') as $cottagefeatures){
               foreach($details->find('ul') as $list){
                 $listArr = explode(":",str_replace("&nbsp;","",$list->plaintext));            
                 if(strpos($listArr[2],"Yes"))
                    $pets = 1;
                   else $pets = 0;
                 $bedrooms = str_replace("Internet","",$listArr[3]);
                 $sleeps = str_replace("Pets","",$listArr[1]);
                 $changeover = $listArr[6];
             }
        }

        
 
        $record = array(
          'COTTAGE_URL'   => "http://www.suffolk-secrets.co.uk".$cottage_URL,
          'COTTAGE_NAME'  => $cottage_name,
          'COTTAGE_ID'    => $cottage_ID,
          'SLEEPS'        => $sleeps,
          'BEDROOMS'      => $bedrooms,
          'PETS'          => $pets,
          'PRICE_LOW'     => $priceLow,
        );   
 
       
        scraperwiki::save(array('COTTAGE_URL'), $record);


      }
    }
}
 $i++;

}
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 37;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.suffolk-secrets.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=search-container]') as $page){
      // cottage

      foreach($page->find('div[class=property_result]') as $cottage){
        $cottage_name = "";
        foreach($cottage->find('div[class=property_right]') as $details){

             # cottage name, URL and ID
             foreach($details->find('h2') as $cottageNameData){
               foreach($details->find('a') as $cottageURLData){
                 if($cottage_name == "")   
                   $cottage_name = $cottageURLData->plaintext;     
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }

             foreach($details->find('span[class=price]') as $priceData){
                 $priceLow = str_replace("&pound;","",$priceData->plaintext);
             }


             # cottage Pets, Bedrooms and Sleeps
             foreach($details->find('div[class=details]') as $cottagefeatures){
               foreach($details->find('ul') as $list){
                 $listArr = explode(":",str_replace("&nbsp;","",$list->plaintext));            
                 if(strpos($listArr[2],"Yes"))
                    $pets = 1;
                   else $pets = 0;
                 $bedrooms = str_replace("Internet","",$listArr[3]);
                 $sleeps = str_replace("Pets","",$listArr[1]);
                 $changeover = $listArr[6];
             }
        }

        
 
        $record = array(
          'COTTAGE_URL'   => "http://www.suffolk-secrets.co.uk".$cottage_URL,
          'COTTAGE_NAME'  => $cottage_name,
          'COTTAGE_ID'    => $cottage_ID,
          'SLEEPS'        => $sleeps,
          'BEDROOMS'      => $bedrooms,
          'PETS'          => $pets,
          'PRICE_LOW'     => $priceLow,
        );   
 
       
        scraperwiki::save(array('COTTAGE_URL'), $record);


      }
    }
}
 $i++;

}
?>
