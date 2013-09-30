<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 35;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.marsdens.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=tabledata]') as $page){
      // cottage
      foreach($page->find('div[class=property]') as $cottage){
        foreach($cottage->find('div[class=property-desc inline-block]') as $details){
             # cottage name, URL and ID
             foreach($details->find('h3') as $cottageNameData){
               $cottage_name = substr($cottageNameData->plaintext,0,strpos($cottageNameData->plaintext,","));
               foreach($details->find('a') as $cottageURLData){
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }
    
             # cottage Pets, Bedrooms and Sleeps
             foreach($details->find('ul[class=attributes]') as $cottagefeatures){
               $petsArray = explode(":",$cottagefeatures);
               if(strpos($petsArray[4],"tick.gif"))
                $pets = 1;
               else $pets = 0;
    
               $featuresArray = explode(":",$cottagefeatures->plaintext);
               $bedrooms = str_replace("Parking","",$featuresArray[1]);
               $sleeps = str_replace("Parking","",$featuresArray[1]);
             }
        }

        foreach($cottage->find('div[class=pricerange clear]') as $priceRange){
          foreach($priceRange->find('h3') as $priceDetails){  
            $priceLow= $priceDetails->plaintext;
            $priceLow = str_replace("&pound;","",$priceLow);
          }  
        }
 
        $record = array(
          'COTTAGE_URL'   => "http://www.marsdens.co.uk".$cottage_URL,
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
 $i++;
}
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 35;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.marsdens.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=tabledata]') as $page){
      // cottage
      foreach($page->find('div[class=property]') as $cottage){
        foreach($cottage->find('div[class=property-desc inline-block]') as $details){
             # cottage name, URL and ID
             foreach($details->find('h3') as $cottageNameData){
               $cottage_name = substr($cottageNameData->plaintext,0,strpos($cottageNameData->plaintext,","));
               foreach($details->find('a') as $cottageURLData){
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }
    
             # cottage Pets, Bedrooms and Sleeps
             foreach($details->find('ul[class=attributes]') as $cottagefeatures){
               $petsArray = explode(":",$cottagefeatures);
               if(strpos($petsArray[4],"tick.gif"))
                $pets = 1;
               else $pets = 0;
    
               $featuresArray = explode(":",$cottagefeatures->plaintext);
               $bedrooms = str_replace("Parking","",$featuresArray[1]);
               $sleeps = str_replace("Parking","",$featuresArray[1]);
             }
        }

        foreach($cottage->find('div[class=pricerange clear]') as $priceRange){
          foreach($priceRange->find('h3') as $priceDetails){  
            $priceLow= $priceDetails->plaintext;
            $priceLow = str_replace("&pound;","",$priceLow);
          }  
        }
 
        $record = array(
          'COTTAGE_URL'   => "http://www.marsdens.co.uk".$cottage_URL,
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
 $i++;
}
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 35;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.marsdens.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=tabledata]') as $page){
      // cottage
      foreach($page->find('div[class=property]') as $cottage){
        foreach($cottage->find('div[class=property-desc inline-block]') as $details){
             # cottage name, URL and ID
             foreach($details->find('h3') as $cottageNameData){
               $cottage_name = substr($cottageNameData->plaintext,0,strpos($cottageNameData->plaintext,","));
               foreach($details->find('a') as $cottageURLData){
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }
    
             # cottage Pets, Bedrooms and Sleeps
             foreach($details->find('ul[class=attributes]') as $cottagefeatures){
               $petsArray = explode(":",$cottagefeatures);
               if(strpos($petsArray[4],"tick.gif"))
                $pets = 1;
               else $pets = 0;
    
               $featuresArray = explode(":",$cottagefeatures->plaintext);
               $bedrooms = str_replace("Parking","",$featuresArray[1]);
               $sleeps = str_replace("Parking","",$featuresArray[1]);
             }
        }

        foreach($cottage->find('div[class=pricerange clear]') as $priceRange){
          foreach($priceRange->find('h3') as $priceDetails){  
            $priceLow= $priceDetails->plaintext;
            $priceLow = str_replace("&pound;","",$priceLow);
          }  
        }
 
        $record = array(
          'COTTAGE_URL'   => "http://www.marsdens.co.uk".$cottage_URL,
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
 $i++;
}
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 35;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.marsdens.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=tabledata]') as $page){
      // cottage
      foreach($page->find('div[class=property]') as $cottage){
        foreach($cottage->find('div[class=property-desc inline-block]') as $details){
             # cottage name, URL and ID
             foreach($details->find('h3') as $cottageNameData){
               $cottage_name = substr($cottageNameData->plaintext,0,strpos($cottageNameData->plaintext,","));
               foreach($details->find('a') as $cottageURLData){
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }
    
             # cottage Pets, Bedrooms and Sleeps
             foreach($details->find('ul[class=attributes]') as $cottagefeatures){
               $petsArray = explode(":",$cottagefeatures);
               if(strpos($petsArray[4],"tick.gif"))
                $pets = 1;
               else $pets = 0;
    
               $featuresArray = explode(":",$cottagefeatures->plaintext);
               $bedrooms = str_replace("Parking","",$featuresArray[1]);
               $sleeps = str_replace("Parking","",$featuresArray[1]);
             }
        }

        foreach($cottage->find('div[class=pricerange clear]') as $priceRange){
          foreach($priceRange->find('h3') as $priceDetails){  
            $priceLow= $priceDetails->plaintext;
            $priceLow = str_replace("&pound;","",$priceLow);
          }  
        }
 
        $record = array(
          'COTTAGE_URL'   => "http://www.marsdens.co.uk".$cottage_URL,
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
 $i++;
}
?>
