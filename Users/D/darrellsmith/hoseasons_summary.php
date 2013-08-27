<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 206;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

  while($i<=$maxpages){

    scraperwiki::save_var("page",$i);
    $url = "http://www.hoseasons.co.uk/cottages/search/all-regions?page=".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);
    // page
    foreach($dom->find('div[class=tab_panel_content]') as $page){

      // cottage name and link
     foreach($page->find('div[class=even]') as $cottage){
    #  foreach($page->find('div[class=odd]') as $cottage){


       $cottage_Name = "N/A";
       $cottage_URL = "N/A";
       foreach($cottage->find('div[class=cottageNameAndLinks]') as $details){
        # cottage name, URL and ID
        foreach($details->find('a') as $cottageURLData){
          if($cottage_Name == "N/A")
             $cottage_Name = strip_tags($cottageURLData); 
          if($cottage_URL == "N/A")
             $cottage_URL = $cottageURLData->href;
          $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
          $cottIDblok = substr($details,strpos($details,"Ref:"),25);
          $cottIDblok = str_replace("Ref:</b>&nbsp;","",$cottIDblok);
          $cottage_ID= substr($cottIDblok,0,strpos($cottIDblok,"<"));
         }
       }
       


       // sleeps, beds, pets
       foreach($cottage->find('div[class=cottageMakeup]') as $priceRange){
        foreach($priceRange->find('div[class=sleepsCount]') as $data){
          $sleeps = $data->plaintext;
        }
        foreach($priceRange->find('div[class=bedroomCount]') as $data){
          $bedrooms = $data->plaintext;
        }
        foreach($priceRange->find('div[class=petCount]') as $data){
          $petscount = $data->plaintext;
          if($petscount != 0)
            $pets = 1;
          else 
            $pets = 0;
        }
       }


       // Price and save record
       foreach($cottage->find('div[class=cottagePrice]') as $priceRange){
        foreach($priceRange->find('div[class=pricesFrom]') as $priceDetails){  
          $priceArr = explode("-",$priceDetails->plaintext);
          $priceLow = str_replace("£","",$priceArr[0]);
          $priceHigh = str_replace("£","",$priceArr[1]);
        }

       $record = array(
        'COTTAGE_URL'   => "http://www.hoseasons.co.uk".$cottage_URL,
        'COTTAGE_NAME'  => $cottage_Name,
        'COTTAGE_ID'    => $cottage_ID,
        'SLEEPS'        => $sleeps,
        'BEDROOMS'      => $bedrooms,
        'PETS'          => $pets,
        'PRICE_LOW'     => $priceLow,
        'PRICE_HIGH'    => $priceHigh,
       );      
}
        # print_r($record);       
      scraperwiki::save(array('COTTAGE_URL'), $record);
}

// page and count
 
    }
   $i++;
  }
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 206;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

  while($i<=$maxpages){

    scraperwiki::save_var("page",$i);
    $url = "http://www.hoseasons.co.uk/cottages/search/all-regions?page=".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);
    // page
    foreach($dom->find('div[class=tab_panel_content]') as $page){

      // cottage name and link
     foreach($page->find('div[class=even]') as $cottage){
    #  foreach($page->find('div[class=odd]') as $cottage){


       $cottage_Name = "N/A";
       $cottage_URL = "N/A";
       foreach($cottage->find('div[class=cottageNameAndLinks]') as $details){
        # cottage name, URL and ID
        foreach($details->find('a') as $cottageURLData){
          if($cottage_Name == "N/A")
             $cottage_Name = strip_tags($cottageURLData); 
          if($cottage_URL == "N/A")
             $cottage_URL = $cottageURLData->href;
          $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
          $cottIDblok = substr($details,strpos($details,"Ref:"),25);
          $cottIDblok = str_replace("Ref:</b>&nbsp;","",$cottIDblok);
          $cottage_ID= substr($cottIDblok,0,strpos($cottIDblok,"<"));
         }
       }
       


       // sleeps, beds, pets
       foreach($cottage->find('div[class=cottageMakeup]') as $priceRange){
        foreach($priceRange->find('div[class=sleepsCount]') as $data){
          $sleeps = $data->plaintext;
        }
        foreach($priceRange->find('div[class=bedroomCount]') as $data){
          $bedrooms = $data->plaintext;
        }
        foreach($priceRange->find('div[class=petCount]') as $data){
          $petscount = $data->plaintext;
          if($petscount != 0)
            $pets = 1;
          else 
            $pets = 0;
        }
       }


       // Price and save record
       foreach($cottage->find('div[class=cottagePrice]') as $priceRange){
        foreach($priceRange->find('div[class=pricesFrom]') as $priceDetails){  
          $priceArr = explode("-",$priceDetails->plaintext);
          $priceLow = str_replace("£","",$priceArr[0]);
          $priceHigh = str_replace("£","",$priceArr[1]);
        }

       $record = array(
        'COTTAGE_URL'   => "http://www.hoseasons.co.uk".$cottage_URL,
        'COTTAGE_NAME'  => $cottage_Name,
        'COTTAGE_ID'    => $cottage_ID,
        'SLEEPS'        => $sleeps,
        'BEDROOMS'      => $bedrooms,
        'PETS'          => $pets,
        'PRICE_LOW'     => $priceLow,
        'PRICE_HIGH'    => $priceHigh,
       );      
}
        # print_r($record);       
      scraperwiki::save(array('COTTAGE_URL'), $record);
}

// page and count
 
    }
   $i++;
  }
?>
<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 206;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

  while($i<=$maxpages){

    scraperwiki::save_var("page",$i);
    $url = "http://www.hoseasons.co.uk/cottages/search/all-regions?page=".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);
    // page
    foreach($dom->find('div[class=tab_panel_content]') as $page){

      // cottage name and link
     foreach($page->find('div[class=even]') as $cottage){
    #  foreach($page->find('div[class=odd]') as $cottage){


       $cottage_Name = "N/A";
       $cottage_URL = "N/A";
       foreach($cottage->find('div[class=cottageNameAndLinks]') as $details){
        # cottage name, URL and ID
        foreach($details->find('a') as $cottageURLData){
          if($cottage_Name == "N/A")
             $cottage_Name = strip_tags($cottageURLData); 
          if($cottage_URL == "N/A")
             $cottage_URL = $cottageURLData->href;
          $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
          $cottIDblok = substr($details,strpos($details,"Ref:"),25);
          $cottIDblok = str_replace("Ref:</b>&nbsp;","",$cottIDblok);
          $cottage_ID= substr($cottIDblok,0,strpos($cottIDblok,"<"));
         }
       }
       


       // sleeps, beds, pets
       foreach($cottage->find('div[class=cottageMakeup]') as $priceRange){
        foreach($priceRange->find('div[class=sleepsCount]') as $data){
          $sleeps = $data->plaintext;
        }
        foreach($priceRange->find('div[class=bedroomCount]') as $data){
          $bedrooms = $data->plaintext;
        }
        foreach($priceRange->find('div[class=petCount]') as $data){
          $petscount = $data->plaintext;
          if($petscount != 0)
            $pets = 1;
          else 
            $pets = 0;
        }
       }


       // Price and save record
       foreach($cottage->find('div[class=cottagePrice]') as $priceRange){
        foreach($priceRange->find('div[class=pricesFrom]') as $priceDetails){  
          $priceArr = explode("-",$priceDetails->plaintext);
          $priceLow = str_replace("£","",$priceArr[0]);
          $priceHigh = str_replace("£","",$priceArr[1]);
        }

       $record = array(
        'COTTAGE_URL'   => "http://www.hoseasons.co.uk".$cottage_URL,
        'COTTAGE_NAME'  => $cottage_Name,
        'COTTAGE_ID'    => $cottage_ID,
        'SLEEPS'        => $sleeps,
        'BEDROOMS'      => $bedrooms,
        'PETS'          => $pets,
        'PRICE_LOW'     => $priceLow,
        'PRICE_HIGH'    => $priceHigh,
       );      
}
        # print_r($record);       
      scraperwiki::save(array('COTTAGE_URL'), $record);
}

// page and count
 
    }
   $i++;
  }
?>
