<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 46;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.norfolkcottages.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=search-results-container]') as $page){
      // cottage
     foreach($dom->find('div[class=property-result-container]') as $page){

      foreach($page->find('div[class=middle-container]') as $cottage){
        $cottage_name = "";
             # cottage name, URL and ID
             foreach($cottage->find('h2') as $cottageNameData){
               foreach($cottageNameData->find('a') as $cottageURLData){
                 if($cottage_name == "")   
                   $cottage_name = substr($cottageURLData->plaintext,0,strpos($cottageURLData->plaintext,"("));     
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }

             foreach($cottage->find('span[class=price]') as $priceData){
                 $priceLow = str_replace("&pound;","",$priceData->plaintext);
             }

             # cottage Pets, Bedrooms and Sleeps
             foreach($cottage->find('div[class=attributes]') as $cottagefeatures){
               foreach($cottagefeatures->find('p') as $list){
                 $listArr = explode("|",str_replace("&nbsp;","",$list->plaintext));            
                 $bedrooms = str_replace("Bedrooms: ","",$listArr[1]);
                 $sleeps = str_replace("Sleeps:","",$listArr[0]);
                 $baths = str_replace("Bathrooms:","",$listArr[2]);
               }
             }
      }

      foreach($page->find('div[class=right-container]') as $cottage){
        foreach($page->find('div[class=price-range]') as $price){
          $lowPrice =  str_replace("&pound;","",$price->plaintext);
          $lowPrice =  str_replace("Per Week","",$lowPrice);
        }
      }


        $record = array(
          'COTTAGE_URL'   => "http://www.norfolkcottages.co.uk".$cottage_URL,
          'COTTAGE_NAME'  => $cottage_name,
          'COTTAGE_ID'    => $cottage_ID,
          'SLEEPS'        => $sleeps,
          'BEDROOMS'      => $bedrooms,
          'BATHROOMS'     => $baths,
          'PRICE_LOW'     => $lowPrice,
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

$maxpages = 46;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.norfolkcottages.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=search-results-container]') as $page){
      // cottage
     foreach($dom->find('div[class=property-result-container]') as $page){

      foreach($page->find('div[class=middle-container]') as $cottage){
        $cottage_name = "";
             # cottage name, URL and ID
             foreach($cottage->find('h2') as $cottageNameData){
               foreach($cottageNameData->find('a') as $cottageURLData){
                 if($cottage_name == "")   
                   $cottage_name = substr($cottageURLData->plaintext,0,strpos($cottageURLData->plaintext,"("));     
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }

             foreach($cottage->find('span[class=price]') as $priceData){
                 $priceLow = str_replace("&pound;","",$priceData->plaintext);
             }

             # cottage Pets, Bedrooms and Sleeps
             foreach($cottage->find('div[class=attributes]') as $cottagefeatures){
               foreach($cottagefeatures->find('p') as $list){
                 $listArr = explode("|",str_replace("&nbsp;","",$list->plaintext));            
                 $bedrooms = str_replace("Bedrooms: ","",$listArr[1]);
                 $sleeps = str_replace("Sleeps:","",$listArr[0]);
                 $baths = str_replace("Bathrooms:","",$listArr[2]);
               }
             }
      }

      foreach($page->find('div[class=right-container]') as $cottage){
        foreach($page->find('div[class=price-range]') as $price){
          $lowPrice =  str_replace("&pound;","",$price->plaintext);
          $lowPrice =  str_replace("Per Week","",$lowPrice);
        }
      }


        $record = array(
          'COTTAGE_URL'   => "http://www.norfolkcottages.co.uk".$cottage_URL,
          'COTTAGE_NAME'  => $cottage_name,
          'COTTAGE_ID'    => $cottage_ID,
          'SLEEPS'        => $sleeps,
          'BEDROOMS'      => $bedrooms,
          'BATHROOMS'     => $baths,
          'PRICE_LOW'     => $lowPrice,
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

$maxpages = 46;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
  $i = $placeholder;
$j = 0;
$counter = 0;

while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.norfolkcottages.co.uk/cottage-search/amount-10/page-".$i;
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages 
    #echo $dom;
    // page
    foreach($dom->find('div[id=search-results-container]') as $page){
      // cottage
     foreach($dom->find('div[class=property-result-container]') as $page){

      foreach($page->find('div[class=middle-container]') as $cottage){
        $cottage_name = "";
             # cottage name, URL and ID
             foreach($cottage->find('h2') as $cottageNameData){
               foreach($cottageNameData->find('a') as $cottageURLData){
                 if($cottage_name == "")   
                   $cottage_name = substr($cottageURLData->plaintext,0,strpos($cottageURLData->plaintext,"("));     
                 $cottage_URL = $cottageURLData->href;
                 $cottage_ID = str_replace("/cottage-details/","",$cottage_URL); 
               }
             }

             foreach($cottage->find('span[class=price]') as $priceData){
                 $priceLow = str_replace("&pound;","",$priceData->plaintext);
             }

             # cottage Pets, Bedrooms and Sleeps
             foreach($cottage->find('div[class=attributes]') as $cottagefeatures){
               foreach($cottagefeatures->find('p') as $list){
                 $listArr = explode("|",str_replace("&nbsp;","",$list->plaintext));            
                 $bedrooms = str_replace("Bedrooms: ","",$listArr[1]);
                 $sleeps = str_replace("Sleeps:","",$listArr[0]);
                 $baths = str_replace("Bathrooms:","",$listArr[2]);
               }
             }
      }

      foreach($page->find('div[class=right-container]') as $cottage){
        foreach($page->find('div[class=price-range]') as $price){
          $lowPrice =  str_replace("&pound;","",$price->plaintext);
          $lowPrice =  str_replace("Per Week","",$lowPrice);
        }
      }


        $record = array(
          'COTTAGE_URL'   => "http://www.norfolkcottages.co.uk".$cottage_URL,
          'COTTAGE_NAME'  => $cottage_name,
          'COTTAGE_ID'    => $cottage_ID,
          'SLEEPS'        => $sleeps,
          'BEDROOMS'      => $bedrooms,
          'BATHROOMS'     => $baths,
          'PRICE_LOW'     => $lowPrice,
        );

        scraperwiki::save(array('COTTAGE_URL'), $record);

    }

}
 $i++;
}
?>
