<?php
    $j=1;
    $i=1;
    while(true){    
         $link="http://www.yeskantipur.com/index.php?route=product/search&filter_name=%&filter_category_id=0&page=".$j;
          $j++;
                   
         $html = file_get_contents($link);
         $dom = new DomDocument();
         @$dom->loadHTML($html);
         $xpath = new DOMXPath($dom);
    
         $mainNodeCollection= $xpath->query("//div[@class='name']/parent::*");
        if(count($mainNodeCollection)<=0) break;
        
        foreach ($mainNodeCollection as $node){
           //echo $node->c14n();
           @$dom->loadHTML($node->c14n());
            $xpath = new DOMXPath($dom);
            $itemName = $xpath->query("//div[@class='name']")->item(0)->nodeValue;
            $itemLink= $xpath->query("//a/@href")->item(0)->nodeValue;        
            $itemPrice= $xpath->query("//div[@class='price']/text()")->item(0)->nodeValue;
            scraperwiki::save_sqlite(array("index"),array("index"=>$i, "Name"=>$itemName,  "Link"=>$itemLink, "Price"=>$itemPrice));
           $i++;
           
        } 
   }
    
     

?>
<?php
    $j=1;
    $i=1;
    while(true){    
         $link="http://www.yeskantipur.com/index.php?route=product/search&filter_name=%&filter_category_id=0&page=".$j;
          $j++;
                   
         $html = file_get_contents($link);
         $dom = new DomDocument();
         @$dom->loadHTML($html);
         $xpath = new DOMXPath($dom);
    
         $mainNodeCollection= $xpath->query("//div[@class='name']/parent::*");
        if(count($mainNodeCollection)<=0) break;
        
        foreach ($mainNodeCollection as $node){
           //echo $node->c14n();
           @$dom->loadHTML($node->c14n());
            $xpath = new DOMXPath($dom);
            $itemName = $xpath->query("//div[@class='name']")->item(0)->nodeValue;
            $itemLink= $xpath->query("//a/@href")->item(0)->nodeValue;        
            $itemPrice= $xpath->query("//div[@class='price']/text()")->item(0)->nodeValue;
            scraperwiki::save_sqlite(array("index"),array("index"=>$i, "Name"=>$itemName,  "Link"=>$itemLink, "Price"=>$itemPrice));
           $i++;
           
        } 
   }
    
     

?>
