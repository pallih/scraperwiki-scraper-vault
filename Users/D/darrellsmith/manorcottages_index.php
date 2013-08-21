<?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 14;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
    $i = $placeholder;
$j = 0;
while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.manorcottages.co.uk/properties/search?commit=Search&page=".$i."&utf8=%E2%9C%93";
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages
    foreach($dom->find('ul[class=results]') as $page)

      $elements ="";
      // Get a cottage

      foreach($page->find('li') as $cottage){
        
        
        foreach($cottage->find('span[class=price]') as $element){
            $priceLow = $element->plaintext;
        }
        $priceLow = str_replace("From &pound;","",$priceLow);
    
        if(strpos($priceLow,"&")!= false){
            $priceLow = substr($priceLow,0,strpos($priceLow,"&"));
        }

        foreach($cottage->find('div[class=details]') as $element)
          foreach($element->find('a') as $fragment)
            $cottageURL = $fragment->href;
       
        foreach($cottage->find('H3') as $element){
            $cottage_name = $element->plaintext;
        }
        
        $cottageID = str_replace("http://www.manorcottages.co.uk/properties/","",$cottageURL );
        foreach($cottage->find('ul[class=property_summary]') as $element)
          foreach($element->find('li') as $item){
            foreach($item->find('span') as $ele){
              $elements .= $ele->plaintext.",";
            }            
          }
        $arr = explode(",",$elements);
        $changeover = $arr[0];
        $sleeps = $arr[1];
        $bedrooms = $arr[2];
        $bathrooms = $arr[3];
        $pets = $arr[4];
        if($pets == "No") $pets = 0;
         else $pets = 1;
      


        $record = array(
            'COTTAGE_URL'   => $cottageURL,
            'COTTAGE_ID'    => $cottageID,
            'COTTAGE_NAME'  => $cottage_name,
            'CHANGEOVER'    => $changeover ,
            #'SLEEPS'        => $sleeps,
            #'BEDROOMS'      => $bedrooms,
            'BATHROOMS'     => $bathrooms,
            'PETS'          => $pets,
            'PRICE_LOW'     => $priceLow,
            );
        scraperwiki::save(array('COTTAGE_URL'), $record);

}
    
$i++;
}
    
    












?><?php

require_once 'scraperwiki/simple_html_dom.php';
scraperwiki::save_var('dummy', 0);

$maxpages = 14;
$i = 1;
$dom = new simple_html_dom();

$placeholder = scraperwiki::get_var("page");
if($placeholder)
    $i = $placeholder;
$j = 0;
while($i<=$maxpages){
    scraperwiki::save_var("page",$i);
    $url = "http://www.manorcottages.co.uk/properties/search?commit=Search&page=".$i."&utf8=%E2%9C%93";
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);

    // get the list of cottages
    foreach($dom->find('ul[class=results]') as $page)

      $elements ="";
      // Get a cottage

      foreach($page->find('li') as $cottage){
        
        
        foreach($cottage->find('span[class=price]') as $element){
            $priceLow = $element->plaintext;
        }
        $priceLow = str_replace("From &pound;","",$priceLow);
    
        if(strpos($priceLow,"&")!= false){
            $priceLow = substr($priceLow,0,strpos($priceLow,"&"));
        }

        foreach($cottage->find('div[class=details]') as $element)
          foreach($element->find('a') as $fragment)
            $cottageURL = $fragment->href;
       
        foreach($cottage->find('H3') as $element){
            $cottage_name = $element->plaintext;
        }
        
        $cottageID = str_replace("http://www.manorcottages.co.uk/properties/","",$cottageURL );
        foreach($cottage->find('ul[class=property_summary]') as $element)
          foreach($element->find('li') as $item){
            foreach($item->find('span') as $ele){
              $elements .= $ele->plaintext.",";
            }            
          }
        $arr = explode(",",$elements);
        $changeover = $arr[0];
        $sleeps = $arr[1];
        $bedrooms = $arr[2];
        $bathrooms = $arr[3];
        $pets = $arr[4];
        if($pets == "No") $pets = 0;
         else $pets = 1;
      


        $record = array(
            'COTTAGE_URL'   => $cottageURL,
            'COTTAGE_ID'    => $cottageID,
            'COTTAGE_NAME'  => $cottage_name,
            'CHANGEOVER'    => $changeover ,
            #'SLEEPS'        => $sleeps,
            #'BEDROOMS'      => $bedrooms,
            'BATHROOMS'     => $bathrooms,
            'PETS'          => $pets,
            'PRICE_LOW'     => $priceLow,
            );
        scraperwiki::save(array('COTTAGE_URL'), $record);

}
    
$i++;
}
    
    












?>