<?php

$linkList = array();
for($j ='A'; ; $j++){
    
     $link="http://www.ufindus.com/".$j;
         
                   
     $html = file_get_contents($link);
     $dom = new DomDocument();
     @$dom->loadHTML($html);
     $xpath = new DOMXPath($dom);

     $mainNodeCollection= $xpath->query("//p[@class='catlist']//a/@href");
    
        foreach ($mainNodeCollection as $node){
            array_push($linkList,'http://www.ufindus.com'.$node->nodeValue);
        } 
    if($j=='Z') break;
    }

?>

<?php
    $i=1;
    foreach($linkList as $link){
       $html = file_get_contents($link);
       $dom = new DomDocument();
       @$dom->loadHTML($html);
       $xpath = new DOMXPath($dom);
       $mainNodeCollection= $xpath->query("//div[@class='paid']");
    
       $mainNodeCollection2= $xpath->query("//div[@class='free_middle']");
    
       foreach($mainNodeCollection as $eachNode){
            @$dom->loadHTML($eachNode->c14n());
            $xpath = new DOMXPath($dom);
            $name =$xpath->query("//h2/a/text()")->item(0)->nodeValue;
            $phone =$xpath->query("//p[@class='paid_phone']")->item(0)->nodeValue;
            $website = $xpath->query("//a[@class='contact_website']/@href")->item(0)->nodeValue;
            $address = $xpath->query("//a[@class='contact_address']/@onclick")->item(0)->nodeValue;
            $addr = explode("',", $address);
            $address = $addr[9];
            scraperwiki::save_sqlite(array("index"),array("index"=>$i, "Name"=>$name, "Phone"=>$phone, "Website"=>$website,"Address"=>$address));
            $i++;
        }
        
    
       foreach($mainNodeCollection2 as $eachNode){
            @$dom->loadHTML($eachNode->c14n());
             $xpath = new DOMXPath($dom);
            $name =$xpath->query("//h4/text()")->item(0)->nodeValue;
            $phone =$xpath->query("//span[@class='tel']")->item(0)->nodeValue;
            //$website = $xpath->query("//a[@class='contact_website']/@href")->item(0)->nodeValue;
            $address = $xpath->query("//span[@class='adr']/text()")->item(0)->nodeValue;
            scraperwiki::save_sqlite(array("index"),array("index"=>$i, "Name"=>$name, "Phone"=>$phone, "Website"=>"","Address"=>$address));
            $i++;
        }
    }    
?>